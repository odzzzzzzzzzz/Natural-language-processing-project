from pathlib import Path
import argparse
import joblib
import sklearn_crfsuite
from datasets import load_dataset

ROOT = Path(__file__).resolve().parents[2]

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

def token_features(tokens, i):
    tok = tokens[i]
    lower = tok.lower()

    feats = {
        "bias": 1.0,
        "word.lower": lower,
        "suffix2": lower[-2:],
        "suffix3": lower[-3:],
        "suffix4": lower[-4:],
        "prefix2": lower[:2],
        "prefix3": lower[:3],
        "is_capitalized": tok[:1].isupper(),
        "is_all_upper": tok.isupper(),
        "is_title_case": tok.istitle(),
        "has_digit": any(c.isdigit() for c in tok),
        "has_period": "." in tok,
        "shape": shape(tok),
    }

    if i == 0:
        feats["BOS"] = True
    else:
        prev = tokens[i - 1]
        feats["prev_word"] = prev.lower()
        feats["prev_shape"] = shape(prev)

    if i == len(tokens) - 1:
        feats["EOS"] = True
    else:
        nxt = tokens[i + 1]
        feats["next_word"] = nxt.lower()
        feats["next_shape"] = shape(nxt)

    if i >= 2:
        feats["prev2_word"] = tokens[i - 2].lower()
    if i + 2 < len(tokens):
        feats["next2_word"] = tokens[i + 2].lower()

    return feats

def sent2features(tokens):
    return [token_features(tokens, i) for i in range(len(tokens))]

def map_conll_label(label):
    """
    Map CoNLL-2003 labels to our legal schema.

    PER -> PARTY
    ORG -> ORG
    LOC, MISC -> O

    This intentionally weak mapping creates an out-of-domain transfer baseline.
    CoNLL has no CITATION, COURT, STATUTE, JUDGE, or DATE labels.
    """
    if label == "O":
        return "O"

    if "-" not in label:
        return "O"

    prefix, typ = label.split("-", 1)

    if typ == "PER":
        return f"{prefix}-PARTY"
    if typ == "ORG":
        return f"{prefix}-ORG"

    return "O"

def load_conll2003(max_train_sents=None):
    print("Loading CoNLL-2003 from HuggingFace datasets...")
    try:
        ds = load_dataset("conll2003", trust_remote_code=True)
    except Exception:
        ds = load_dataset("eriktks/conll2003", trust_remote_code=True)

    label_names = ds["train"].features["ner_tags"].feature.names

    X_train = []
    y_train = []

    train_data = ds["train"]
    if max_train_sents is not None and max_train_sents > 0:
        train_data = train_data.select(range(min(max_train_sents, len(train_data))))

    for ex in train_data:
        tokens = ex["tokens"]
        labels = [map_conll_label(label_names[i]) for i in ex["ner_tags"]]

        X_train.append(sent2features(tokens))
        y_train.append(labels)

    print(f"Loaded CoNLL training sentences: {len(X_train)}")
    return X_train, y_train

def read_legal_test(path):
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
            token = parts[0]
            gold = parts[-1] if len(parts) == 2 else parts[-2]

            cur.append({"token": token, "gold": gold})

    if cur:
        sentences.append(cur)

    return sentences

def write_predictions(sentences, predictions, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for sent, pred_sent in zip(sentences, predictions):
            for item, pred in zip(sent, pred_sent):
                f.write(f"{item['token']}\t{item['gold']}\t{pred}\n")
            f.write("\n")

def train_crf(X_train, y_train):
    print("Training CoNLL-2003 CRF transfer baseline...")
    crf = sklearn_crfsuite.CRF(
        algorithm="lbfgs",
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True,
    )
    crf.fit(X_train, y_train)
    return crf

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--legal_test", default="data/splits/test.conll")
    parser.add_argument("--output", default="data/splits/test_conll2003_crf_pred.conll")
    parser.add_argument("--model_out", default="models/conll2003_crf_transfer.pkl")
    parser.add_argument(
        "--max_train_sents",
        type=int,
        default=5000,
        help="Use 0 for full CoNLL-2003 train set. Default 5000 for faster baseline training."
    )
    args = parser.parse_args()

    max_train = None if args.max_train_sents == 0 else args.max_train_sents

    X_train, y_train = load_conll2003(max_train_sents=max_train)

    crf = train_crf(X_train, y_train)

    model_out = ROOT / args.model_out
    model_out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(crf, model_out)
    print(f"Saved model to {model_out}")

    legal_sentences = read_legal_test(ROOT / args.legal_test)
    X_legal = [sent2features([x["token"] for x in sent]) for sent in legal_sentences]

    print(f"Predicting on legal test sentences/passages: {len(legal_sentences)}")
    preds = crf.predict(X_legal)

    output_path = ROOT / args.output
    write_predictions(legal_sentences, preds, output_path)
    print(f"Saved predictions to {output_path}")

if __name__ == "__main__":
    main()
