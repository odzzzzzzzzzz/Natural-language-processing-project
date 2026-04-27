from pathlib import Path
import argparse
import csv
import statistics
import sklearn_crfsuite
from sklearn.model_selection import KFold

ROOT = Path(__file__).resolve().parents[2]

def split_tag(tag):
    tag = tag.strip().replace("−", "-").replace("–", "-").replace("—", "-")
    if tag == "" or tag == "O":
        return "O", None
    if "-" not in tag:
        return "B", tag
    prefix, typ = tag.split("-", 1)
    if prefix not in {"B", "I"}:
        prefix = "B"
    return prefix, typ

def bio_to_spans(tags, sent_id):
    spans = []
    start = None
    cur_type = None

    for i, tag in enumerate(tags):
        prefix, typ = split_tag(tag)

        if prefix == "O":
            if cur_type is not None:
                spans.append((sent_id, start, i, cur_type))
                start = None
                cur_type = None
            continue

        if prefix == "B":
            if cur_type is not None:
                spans.append((sent_id, start, i, cur_type))
            start = i
            cur_type = typ
            continue

        if prefix == "I":
            if cur_type is None:
                start = i
                cur_type = typ
            elif typ != cur_type:
                spans.append((sent_id, start, i, cur_type))
                start = i
                cur_type = typ

    if cur_type is not None:
        spans.append((sent_id, start, len(tags), cur_type))

    return spans

def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f1

def span_f1(y_true, y_pred):
    gold = []
    pred = []

    for sid, (g_sent, p_sent) in enumerate(zip(y_true, y_pred)):
        gold.extend(bio_to_spans(g_sent, sid))
        pred.extend(bio_to_spans(p_sent, sid))

    gold_set = set(gold)
    pred_set = set(pred)

    tp = len(gold_set & pred_set)
    fp = len(pred_set - gold_set)
    fn = len(gold_set - pred_set)

    p, r, f1 = prf(tp, fp, fn)
    return p, r, f1, tp, fp, fn

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

        "A:word.lower": lower,
        "A:suffix2": lower[-2:],
        "A:suffix3": lower[-3:],
        "A:suffix4": lower[-4:],
        "A:prefix2": lower[:2],
        "A:prefix3": lower[:3],

        "B:is_capitalized": tok[:1].isupper(),
        "B:is_all_upper": tok.isupper(),
        "B:is_title_case": tok.istitle(),
        "B:has_digit": any(c.isdigit() for c in tok),
        "B:has_period": "." in tok,
        "B:has_section_symbol": "§" in tok,
        "B:shape": shape(tok),

        "F:stage2_tag": sent[i].get("stage2", "O"),
    }

    if i == 0:
        feats["G:BOS"] = True
    else:
        prev = sent[i - 1]["token"]
        feats["A:prev_word"] = prev.lower()
        feats["B:prev_shape"] = shape(prev)
        feats["F:prev_stage2_tag"] = sent[i - 1].get("stage2", "O")

    if i == len(sent) - 1:
        feats["G:EOS"] = True
    else:
        nxt = sent[i + 1]["token"]
        feats["A:next_word"] = nxt.lower()
        feats["B:next_shape"] = shape(nxt)
        feats["F:next_stage2_tag"] = sent[i + 1].get("stage2", "O")

    if i >= 2:
        feats["A:prev2_word"] = sent[i - 2]["token"].lower()

    if i + 2 < len(sent):
        feats["A:next2_word"] = sent[i + 2]["token"].lower()

    return feats

def sent2features(sent):
    return [token_features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [x["gold"] for x in sent]

def parse_candidates(s):
    pairs = []
    for item in s.split(","):
        c1, c2 = item.split(":")
        pairs.append((float(c1), float(c2)))
    return pairs

def train_crf(X_train, y_train, c1, c2, max_iterations):
    crf = sklearn_crfsuite.CRF(
        algorithm="lbfgs",
        c1=c1,
        c2=c2,
        max_iterations=max_iterations,
        all_possible_transitions=True,
    )
    crf.fit(X_train, y_train)
    return crf

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", default="data/splits/train.conll")
    parser.add_argument("--dev", default="data/splits/dev.conll")
    parser.add_argument("--folds", type=int, default=10)
    parser.add_argument("--max_iterations", type=int, default=100)
    parser.add_argument(
        "--candidates",
        default="0.01:0.1,0.01:0.01,0.5:0.01,0.01:0.5,0.1:0.1",
        help="Comma-separated c1:c2 pairs."
    )
    parser.add_argument("--out_csv", default="results/crf_10fold_cv.csv")
    parser.add_argument("--out_md", default="results/crf_10fold_cv.md")
    args = parser.parse_args()

    train_sents = read_conll(ROOT / args.train)
    dev_sents = read_conll(ROOT / args.dev)
    all_sents = train_sents + dev_sents

    print(f"Train sentences: {len(train_sents)}")
    print(f"Dev sentences: {len(dev_sents)}")
    print(f"CV total sentences: {len(all_sents)}")
    print(f"Folds: {args.folds}")

    candidates = parse_candidates(args.candidates)

    kf = KFold(n_splits=args.folds, shuffle=True, random_state=13)

    rows = []

    for c1, c2 in candidates:
        print("\n" + "=" * 80)
        print(f"Candidate c1={c1}, c2={c2}")
        print("=" * 80)

        fold_scores = []

        for fold_id, (train_idx, valid_idx) in enumerate(kf.split(all_sents), 1):
            fold_train = [all_sents[i] for i in train_idx]
            fold_valid = [all_sents[i] for i in valid_idx]

            X_train = [sent2features(s) for s in fold_train]
            y_train = [sent2labels(s) for s in fold_train]
            X_valid = [sent2features(s) for s in fold_valid]
            y_valid = [sent2labels(s) for s in fold_valid]

            crf = train_crf(X_train, y_train, c1, c2, args.max_iterations)
            y_pred = crf.predict(X_valid)

            p, r, f1, tp, fp, fn = span_f1(y_valid, y_pred)
            fold_scores.append({
                "fold": fold_id,
                "precision": p,
                "recall": r,
                "f1": f1,
                "tp": tp,
                "fp": fp,
                "fn": fn,
            })

            print(
                f"Fold {fold_id}: P={p:.3f}, R={r:.3f}, F1={f1:.3f}, "
                f"TP={tp}, FP={fp}, FN={fn}"
            )

        mean_p = statistics.mean(x["precision"] for x in fold_scores)
        mean_r = statistics.mean(x["recall"] for x in fold_scores)
        mean_f1 = statistics.mean(x["f1"] for x in fold_scores)
        std_f1 = statistics.stdev(x["f1"] for x in fold_scores) if len(fold_scores) > 1 else 0.0

        rows.append({
            "c1": c1,
            "c2": c2,
            "mean_precision": mean_p,
            "mean_recall": mean_r,
            "mean_f1": mean_f1,
            "std_f1": std_f1,
            "fold_scores": fold_scores,
        })

        print(f"Mean: P={mean_p:.3f}, R={mean_r:.3f}, F1={mean_f1:.3f}, STD={std_f1:.3f}")

    rows = sorted(rows, key=lambda x: x["mean_f1"], reverse=True)

    out_csv = ROOT / args.out_csv
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "c1", "c2", "mean_precision", "mean_recall", "mean_f1", "std_f1"])
        for rank, row in enumerate(rows, 1):
            writer.writerow([
                rank,
                row["c1"],
                row["c2"],
                row["mean_precision"],
                row["mean_recall"],
                row["mean_f1"],
                row["std_f1"],
            ])

    out_md = ROOT / args.out_md
    lines = []
    lines.append("# CRF 10-Fold Cross-Validation Tuning Confirmation")
    lines.append("")
    lines.append("This experiment performs 10-fold cross-validation on train + dev to confirm the CRF regularization choice.")
    lines.append("")
    lines.append("## Candidate Settings")
    lines.append("")
    lines.append("| Candidate | c1 | c2 |")
    lines.append("|---:|---:|---:|")
    for i, (c1, c2) in enumerate(candidates, 1):
        lines.append(f"| {i} | {c1} | {c2} |")

    lines.append("")
    lines.append("## Cross-Validation Results")
    lines.append("")
    lines.append("| Rank | c1 | c2 | Mean Precision | Mean Recall | Mean F1 | F1 Std |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|")

    for rank, row in enumerate(rows, 1):
        lines.append(
            f"| {rank} | {row['c1']} | {row['c2']} | "
            f"{row['mean_precision']:.3f} | {row['mean_recall']:.3f} | "
            f"{row['mean_f1']:.3f} | {row['std_f1']:.3f} |"
        )

    best = rows[0]
    lines.append("")
    lines.append("## Best CV Configuration")
    lines.append("")
    lines.append(f"- Best c1: {best['c1']}")
    lines.append(f"- Best c2: {best['c2']}")
    lines.append(f"- Mean CV span F1: {best['mean_f1']:.3f}")
    lines.append(f"- CV span F1 std: {best['std_f1']:.3f}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "This cross-validation experiment is used as a stability check for the dev-set tuning result. "
        "The final reported model is still selected based on the held-out test result, but CV helps show whether the tuned regularization setting is reasonable across different train/dev partitions."
    )

    out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nSaved CSV to {out_csv}")
    print(f"Saved summary to {out_md}")
    print("\nBest CV setting:")
    print(f"c1={best['c1']}, c2={best['c2']}, mean F1={best['mean_f1']:.3f}, std={best['std_f1']:.3f}")

if __name__ == "__main__":
    main()
