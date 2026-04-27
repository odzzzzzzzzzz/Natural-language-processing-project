from pathlib import Path
import argparse
import joblib
import nltk
import sklearn_crfsuite

ROOT = Path(__file__).resolve().parents[2]

CHUNK_GRAMMAR = r"""
NP: {<DT|PRP\$>?<JJ.*>*<NN.*|NNP.*>+}
PP: {<IN>}
VP: {<VB.*><RB.*>*}
"""

def ensure_nltk():
    try:
        nltk.pos_tag(["test"])
    except LookupError:
        nltk.download("averaged_perceptron_tagger_eng")
        nltk.download("averaged_perceptron_tagger")

def read_conll(path):
    sentences = []
    cur = []

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")

            if not line.strip():
                if cur:
                    sentences.append(cur)
                    cur = []
                continue

            parts = line.split("\t")

            if len(parts) == 2:
                token, gold = parts
                stage2 = "O"
            elif len(parts) >= 3:
                token, gold, stage2 = parts[0], parts[-2], parts[-1]
            else:
                continue

            cur.append({
                "token": token,
                "gold": gold,
                "stage2": stage2,
            })

    if cur:
        sentences.append(cur)

    return sentences

def tree_to_bio_chunks(tree):
    tags = []

    for node in tree:
        if isinstance(node, nltk.Tree):
            label = node.label()
            leaves = node.leaves()

            for i, _ in enumerate(leaves):
                prefix = "B" if i == 0 else "I"
                tags.append(f"{prefix}-{label}")
        else:
            tags.append("O")

    return tags

def add_pos_and_chunk_tags(sentences):
    parser = nltk.RegexpParser(CHUNK_GRAMMAR)
    token_sents = [[x["token"] for x in sent] for sent in sentences]
    tagged_sents = nltk.pos_tag_sents(token_sents)

    for sent, tagged in zip(sentences, tagged_sents):
        tree = parser.parse(tagged)
        chunk_tags = tree_to_bio_chunks(tree)

        for item, (_, pos), chunk in zip(sent, tagged, chunk_tags):
            item["pos"] = pos
            item["chunk"] = chunk

    return sentences

def shape(word):
    out = []
    for ch in word:
        if ch.isupper():
            out.append("X")
        elif ch.islower():
            out.append("x")
        elif ch.isdigit():
            out.append("d")
        else:
            out.append(ch)
    return "".join(out)

def token_features(sent, i):
    tok = sent[i]["token"]
    lower = tok.lower()
    pos = sent[i].get("pos", "UNK")
    chunk = sent[i].get("chunk", "O")

    feats = {
        "bias": 1.0,

        # Group A: lexical/context
        "A:word.lower": lower,
        "A:suffix2": lower[-2:],
        "A:suffix3": lower[-3:],
        "A:suffix4": lower[-4:],
        "A:prefix2": lower[:2],
        "A:prefix3": lower[:3],

        # Group B: orthographic
        "B:is_capitalized": tok[:1].isupper(),
        "B:is_all_upper": tok.isupper(),
        "B:is_title_case": tok.istitle(),
        "B:has_digit": any(c.isdigit() for c in tok),
        "B:has_period": "." in tok,
        "B:has_section_symbol": "§" in tok,
        "B:shape": shape(tok),

        # Group C/D support: POS and chunk
        # We include POS lightly because the chunker is POS-derived.
        "C:pos": pos,
        "D:chunk": chunk,
        "D:chunk_type": chunk.split("-", 1)[-1] if "-" in chunk else chunk,
        "D:is_np": chunk.endswith("NP"),
        "D:is_vp": chunk.endswith("VP"),
        "D:is_pp": chunk.endswith("PP"),

        # Group F: rule/stage2 output if available
        "F:stage2_tag": sent[i].get("stage2", "O"),
    }

    if i == 0:
        feats["G:BOS"] = True
    else:
        prev = sent[i - 1]["token"]
        feats["A:prev_word"] = prev.lower()
        feats["B:prev_shape"] = shape(prev)
        feats["C:prev_pos"] = sent[i - 1].get("pos", "UNK")
        feats["D:prev_chunk"] = sent[i - 1].get("chunk", "O")
        feats["F:prev_stage2_tag"] = sent[i - 1].get("stage2", "O")

    if i == len(sent) - 1:
        feats["G:EOS"] = True
    else:
        nxt = sent[i + 1]["token"]
        feats["A:next_word"] = nxt.lower()
        feats["B:next_shape"] = shape(nxt)
        feats["C:next_pos"] = sent[i + 1].get("pos", "UNK")
        feats["D:next_chunk"] = sent[i + 1].get("chunk", "O")
        feats["F:next_stage2_tag"] = sent[i + 1].get("stage2", "O")

    if i >= 2:
        feats["A:prev2_word"] = sent[i - 2]["token"].lower()
        feats["D:prev2_chunk"] = sent[i - 2].get("chunk", "O")

    if i + 2 < len(sent):
        feats["A:next2_word"] = sent[i + 2]["token"].lower()
        feats["D:next2_chunk"] = sent[i + 2].get("chunk", "O")

    return feats

def sent2features(sent):
    return [token_features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [x["gold"] for x in sent]

def write_predictions(sentences, predictions, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for sent, pred_sent in zip(sentences, predictions):
            for item, pred in zip(sent, pred_sent):
                f.write(f"{item['token']}\t{item['gold']}\t{pred}\n")
            f.write("\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", default="data/splits/train.conll")
    parser.add_argument("--dev", default="data/splits/dev.conll")
    parser.add_argument("--test", default="data/splits/test.conll")
    parser.add_argument("--output", default="data/splits/test_crf_chunk_pred.conll")
    parser.add_argument("--model_out", default="models/crf_chunk.pkl")
    parser.add_argument("--c1", type=float, default=0.01)
    parser.add_argument("--c2", type=float, default=0.1)
    parser.add_argument("--max_iterations", type=int, default=100)
    args = parser.parse_args()

    ensure_nltk()

    train_sents = read_conll(ROOT / args.train)
    dev_sents = read_conll(ROOT / args.dev)
    test_sents = read_conll(ROOT / args.test)

    train_dev_sents = train_sents + dev_sents

    print(f"Train sentences: {len(train_sents)}")
    print(f"Dev sentences: {len(dev_sents)}")
    print(f"Train+Dev sentences: {len(train_dev_sents)}")
    print(f"Test sentences: {len(test_sents)}")

    print("Adding POS and regex chunk tags...")
    train_dev_sents = add_pos_and_chunk_tags(train_dev_sents)
    test_sents = add_pos_and_chunk_tags(test_sents)

    X_train = [sent2features(s) for s in train_dev_sents]
    y_train = [sent2labels(s) for s in train_dev_sents]
    X_test = [sent2features(s) for s in test_sents]

    print(f"Training chunk-augmented CRF with c1={args.c1}, c2={args.c2}...")
    crf = sklearn_crfsuite.CRF(
        algorithm="lbfgs",
        c1=args.c1,
        c2=args.c2,
        max_iterations=args.max_iterations,
        all_possible_transitions=True,
    )
    crf.fit(X_train, y_train)

    model_out = ROOT / args.model_out
    model_out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(crf, model_out)
    print(f"Saved model to {model_out}")

    print("Predicting test set...")
    preds = crf.predict(X_test)

    output = ROOT / args.output
    write_predictions(test_sents, preds, output)
    print(f"Saved predictions to {output}")

if __name__ == "__main__":
    main()
