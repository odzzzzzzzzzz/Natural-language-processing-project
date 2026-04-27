from pathlib import Path
import re
import csv
import sklearn_crfsuite
from sklearn_crfsuite import metrics

TRAIN_FILE = Path("data/splits/train.conll")
DEV_FILE = Path("data/splits/dev.conll")
OUT_CSV = Path("results/ablation.csv")
OUT_MD = Path("results/ablation.md")

GROUPS = ["A", "B", "F", "G"]

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
        tok, gold = parts[:2]
        stage2 = parts[2] if len(parts) >= 3 else "O"
        sent.append({"token": tok, "gold": gold, "stage2": stage2})
    if sent:
        sents.append(sent)
    return sents

def token_features(sent, i, disabled=None):
    disabled = disabled or set()
    tok = sent[i]["token"]
    lower = tok.lower()
    feats = {"bias": 1.0}

    if "A" not in disabled:
        feats.update({
            "A:word.lower": lower,
            "A:suffix2": lower[-2:],
            "A:suffix3": lower[-3:],
            "A:suffix4": lower[-4:],
            "A:prefix2": lower[:2],
            "A:prefix3": lower[:3],
        })

    if "B" not in disabled:
        feats.update({
            "B:is_capitalized": tok[:1].isupper(),
            "B:is_all_upper": tok.isupper(),
            "B:is_title_case": tok.istitle(),
            "B:has_digit": any(c.isdigit() for c in tok),
            "B:has_period": "." in tok,
            "B:has_section_symbol": "§" in tok,
            "B:shape": shape(tok),
        })

    if "F" not in disabled:
        feats["F:stage2_tag"] = sent[i].get("stage2", "O")

    if i == 0:
        if "G" not in disabled:
            feats["G:BOS"] = True
    else:
        prev = sent[i-1]["token"]
        if "A" not in disabled:
            feats["A:prev_word"] = prev.lower()
        if "B" not in disabled:
            feats["B:prev_shape"] = shape(prev)
        if "F" not in disabled:
            feats["F:prev_stage2_tag"] = sent[i-1].get("stage2", "O")

    if i == len(sent) - 1:
        if "G" not in disabled:
            feats["G:EOS"] = True
    else:
        nxt = sent[i+1]["token"]
        if "A" not in disabled:
            feats["A:next_word"] = nxt.lower()
        if "B" not in disabled:
            feats["B:next_shape"] = shape(nxt)
        if "F" not in disabled:
            feats["F:next_stage2_tag"] = sent[i+1].get("stage2", "O")

    if "A" not in disabled:
        if i >= 2:
            feats["A:prev2_word"] = sent[i-2]["token"].lower()
        if i + 2 < len(sent):
            feats["A:next2_word"] = sent[i+2]["token"].lower()

    return feats

def sent_features(sent, disabled=None):
    return [token_features(sent, i, disabled) for i in range(len(sent))]

def sent_labels(sent):
    return [x["gold"] for x in sent]

def train_eval(disabled=None):
    disabled = disabled or set()
    train_sents = read_conll(TRAIN_FILE)
    dev_sents = read_conll(DEV_FILE)

    X_train = [sent_features(s, disabled) for s in train_sents]
    y_train = [sent_labels(s) for s in train_sents]
    X_dev = [sent_features(s, disabled) for s in dev_sents]
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

    labels = [l for l in crf.classes_ if l != "O"]
    f1 = metrics.flat_f1_score(y_dev, y_pred, average="micro", labels=labels)
    return f1

def main():
    results = []

    full_f1 = train_eval(set())
    results.append(("All features", "", full_f1, 0.0))

    for g in GROUPS:
        f1 = train_eval({g})
        results.append((f"Without group {g}", g, f1, full_f1 - f1))

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["setting", "disabled_group", "dev_micro_f1", "f1_drop"])
        writer.writerows(results)

    lines = ["# CRF Feature Ablation", "", "| Setting | Disabled Group | Dev Micro-F1 | F1 Drop |", "|---|---:|---:|---:|"]
    for setting, group, f1, drop in results:
        lines.append(f"| {setting} | {group} | {f1:.3f} | {drop:.3f} |")

    md = "\n".join(lines)
    OUT_MD.write_text(md + "\n", encoding="utf-8")

    print(md)
    print(f"\nSaved {OUT_CSV}")
    print(f"Saved {OUT_MD}")

if __name__ == "__main__":
    main()
