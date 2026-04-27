from pathlib import Path
import argparse
import joblib
import sklearn_crfsuite

ROOT = Path(__file__).resolve().parents[2]

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
            elif len(parts) >= 3:
                token, gold = parts[0], parts[-2]
            else:
                continue

            cur.append({
                "token": token,
                "gold": gold,
            })

    if cur:
        sentences.append(cur)

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

    feats = {
        "bias": 1.0,

        # Group A: lexical/contextual features
        "A:word.lower": lower,
        "A:suffix2": lower[-2:],
        "A:suffix3": lower[-3:],
        "A:suffix4": lower[-4:],
        "A:prefix2": lower[:2],
        "A:prefix3": lower[:3],

        # Group B: orthographic features
        "B:is_capitalized": tok[:1].isupper(),
        "B:is_all_upper": tok.isupper(),
        "B:is_title_case": tok.istitle(),
        "B:has_digit": any(c.isdigit() for c in tok),
        "B:has_period": "." in tok,
        "B:has_section_symbol": "§" in tok,
        "B:shape": shape(tok),

        # IMPORTANT:
        # No Group F / Stage 2 rule-output feature is included here.
    }

    if i == 0:
        feats["G:BOS"] = True
    else:
        prev = sent[i - 1]["token"]
        feats["A:prev_word"] = prev.lower()
        feats["B:prev_shape"] = shape(prev)

    if i == len(sent) - 1:
        feats["G:EOS"] = True
    else:
        nxt = sent[i + 1]["token"]
        feats["A:next_word"] = nxt.lower()
        feats["B:next_shape"] = shape(nxt)

    if i >= 2:
        feats["A:prev2_word"] = sent[i - 2]["token"].lower()

    if i + 2 < len(sent):
        feats["A:next2_word"] = sent[i + 2]["token"].lower()

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
    parser.add_argument("--output", default="data/splits/test_crf_no_stage2_pred.conll")
    parser.add_argument("--model_out", default="models/crf_no_stage2.pkl")
    parser.add_argument("--c1", type=float, default=0.01)
    parser.add_argument("--c2", type=float, default=0.1)
    parser.add_argument("--max_iterations", type=int, default=100)
    args = parser.parse_args()

    train_sents = read_conll(ROOT / args.train)
    dev_sents = read_conll(ROOT / args.dev)
    test_sents = read_conll(ROOT / args.test)

    train_dev_sents = train_sents + dev_sents

    print(f"Train sentences: {len(train_sents)}")
    print(f"Dev sentences: {len(dev_sents)}")
    print(f"Train+Dev sentences: {len(train_dev_sents)}")
    print(f"Test sentences: {len(test_sents)}")

    X_train = [sent2features(s) for s in train_dev_sents]
    y_train = [sent2labels(s) for s in train_dev_sents]
    X_test = [sent2features(s) for s in test_sents]

    print(f"Training no-stage2 CRF with c1={args.c1}, c2={args.c2}...")
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
