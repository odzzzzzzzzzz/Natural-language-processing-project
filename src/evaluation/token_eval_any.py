from pathlib import Path
import argparse
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]

def split_tag(tag):
    tag = tag.strip().replace("−", "-").replace("–", "-").replace("—", "-")
    if tag == "" or tag == "O":
        return "O"
    if "-" not in tag:
        return tag
    return tag.split("-", 1)[1]

def read_prediction_file(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue

            parts = line.split("\t")
            if len(parts) < 3:
                continue

            token = parts[0]
            gold = parts[-2]
            pred = parts[-1]
            rows.append((token, gold, pred))

    return rows

def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f1

def evaluate(path, model):
    rows = read_prediction_file(path)

    labels = sorted({
        split_tag(gold)
        for _, gold, _ in rows
        if split_tag(gold) != "O"
    } | {
        split_tag(pred)
        for _, _, pred in rows
        if split_tag(pred) != "O"
    })

    counts = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})

    micro_tp = micro_fp = micro_fn = 0

    for _, gold_tag, pred_tag in rows:
        gold = split_tag(gold_tag)
        pred = split_tag(pred_tag)

        if gold == "O" and pred == "O":
            continue

        if pred != "O" and pred == gold:
            counts[pred]["tp"] += 1
            micro_tp += 1

        elif pred != "O" and pred != gold:
            counts[pred]["fp"] += 1
            micro_fp += 1

            if gold != "O":
                counts[gold]["fn"] += 1
                micro_fn += 1

        elif pred == "O" and gold != "O":
            counts[gold]["fn"] += 1
            micro_fn += 1

    lines = []
    lines.append(f"# Token-Level Evaluation: {model}")
    lines.append("")
    lines.append("## Overall")
    lines.append("")
    lines.append("| Model | Precision | Recall | F1 | TP | FP | FN |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")

    p, r, f1 = prf(micro_tp, micro_fp, micro_fn)
    lines.append(f"| {model} | {p:.3f} | {r:.3f} | {f1:.3f} | {micro_tp} | {micro_fp} | {micro_fn} |")

    lines.append("")
    lines.append("## Per-Entity Type")
    lines.append("")
    lines.append("| Entity Type | Precision | Recall | F1 | TP | FP | FN |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")

    for label in labels:
        tp = counts[label]["tp"]
        fp = counts[label]["fp"]
        fn = counts[label]["fn"]
        lp, lr, lf1 = prf(tp, fp, fn)
        lines.append(f"| {label} | {lp:.3f} | {lr:.3f} | {lf1:.3f} | {tp} | {fp} | {fn} |")

    report = "\n".join(lines)

    out = ROOT / f"results/token_eval_{model}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(report, encoding="utf-8")

    print(report)
    print()
    print(f"Saved to {out.relative_to(ROOT)}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--model", required=True)
    args = parser.parse_args()

    evaluate(ROOT / args.input, args.model)

if __name__ == "__main__":
    main()
