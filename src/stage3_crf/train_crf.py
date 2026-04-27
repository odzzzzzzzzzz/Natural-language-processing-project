from pathlib import Path
import re
import joblib
import sklearn_crfsuite
from sklearn_crfsuite import metrics

TRAIN_FILE = Path("data/splits/train.conll")
DEV_FILE = Path("data/splits/dev.conll")
MODEL_FILE = Path("models/crf_v1.pkl")
REPORT_FILE = Path("results/crf_dev_report.txt")

def shape(word):
    s = re.sub(r"[A-Z]", "X", word)
    s = re.sub(r"[a-z]", "x", s)
    s = re.sub(r"[0-9]", "d", s)
    return s

def read_conll(path):
    sents, sent = [], []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            if sent:
                sents.append(sent)
                sent = []
            continue
        parts = line.split("\t")
        if len(parts) == 2:
            tok, gold = parts
            sent.append({"token": tok, "gold": gold, "stage2": "O"})
        elif len(parts) == 3:
            tok, gold, stage2 = parts
            sent.append({"token": tok, "gold": gold, "stage2": stage2})
    if sent:
        sents.append(sent)
    return sents

def token_features(sent, i):
    tok = sent[i]["token"]
    lower = tok.lower()

    feats = {
        "bias": 1.0,

        # GROUP A lexical
        "A:word.lower": lower,
        "A:suffix2": lower[-2:],
        "A:suffix3": lower[-3:],
        "A:suffix4": lower[-4:],
        "A:prefix2": lower[:2],
        "A:prefix3": lower[:3],

        # GROUP B orthographic
        "B:is_capitalized": tok[:1].isupper(),
        "B:is_all_upper": tok.isupper(),
        "B:is_title_case": tok.istitle(),
        "B:has_digit": any(c.isdigit() for c in tok),
        "B:has_period": "." in tok,
        "B:has_section_symbol": "§" in tok,
        "B:shape": shape(tok),

        # GROUP F stage2 output
        "F:stage2_tag": sent[i].get("stage2", "O"),
    }

    if i == 0:
        feats["G:BOS"] = True
    else:
        prev = sent[i-1]["token"]
        feats["A:prev_word"] = prev.lower()
        feats["B:prev_shape"] = shape(prev)
        feats["F:prev_stage2_tag"] = sent[i-1].get("stage2", "O")

    if i == len(sent) - 1:
        feats["G:EOS"] = True
    else:
        nxt = sent[i+1]["token"]
        feats["A:next_word"] = nxt.lower()
        feats["B:next_shape"] = shape(nxt)
        feats["F:next_stage2_tag"] = sent[i+1].get("stage2", "O")

    if i >= 2:
        feats["A:prev2_word"] = sent[i-2]["token"].lower()
    if i + 2 < len(sent):
        feats["A:next2_word"] = sent[i+2]["token"].lower()

    return feats

def sent_features(sent):
    return [token_features(sent, i) for i in range(len(sent))]

def sent_labels(sent):
    return [tok["gold"] for tok in sent]

def main():
    train_sents = read_conll(TRAIN_FILE)
    dev_sents = read_conll(DEV_FILE)

    X_train = [sent_features(s) for s in train_sents]
    y_train = [sent_labels(s) for s in train_sents]
    X_dev = [sent_features(s) for s in dev_sents]
    y_dev = [sent_labels(s) for s in dev_sents]

    crf = sklearn_crfsuite.CRF(
        algorithm="lbfgs",
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True,
    )

    crf.fit(X_train, y_train)
    y_pred = crf.predict(X_dev)

    labels = sorted([l for l in crf.classes_ if l != "O"])

    report = metrics.flat_classification_report(
        y_dev,
        y_pred,
        labels=labels,
        digits=3,
        zero_division=0,
    )

    print(report)
    REPORT_FILE.write_text(report, encoding="utf-8")
    joblib.dump(crf, MODEL_FILE)

    print(f"Saved model to {MODEL_FILE}")
    print(f"Saved report to {REPORT_FILE}")

if __name__ == "__main__":
    main()
