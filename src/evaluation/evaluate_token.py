from pathlib import Path
from collections import Counter

INPUT_FILE = Path("data/splits/test_rule_pred.conll")
REPORT_FILE = Path("results/rule_baseline_report.txt")

def read_labels(path):
    golds = []
    preds = []

    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        _, gold, pred = parts
        golds.append(gold)
        preds.append(pred)

    return golds, preds

def entity_type(tag):
    if tag == "O":
        return "O"
    return tag.split("-", 1)[1]

def compute_token_metrics(golds, preds):
    labels = sorted({
        entity_type(t)
        for t in golds + preds
        if entity_type(t) != "O"
    })

    lines = []
    total_tp = total_fp = total_fn = 0

    for lab in labels:
        tp = fp = fn = 0

        for g, p in zip(golds, preds):
            g_match = entity_type(g) == lab
            p_match = entity_type(p) == lab

            if g_match and p_match:
                tp += 1
            elif not g_match and p_match:
                fp += 1
            elif g_match and not p_match:
                fn += 1

        total_tp += tp
        total_fp += fp
        total_fn += fn

        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

        lines.append(f"{lab:12s} P={precision:.3f} R={recall:.3f} F1={f1:.3f}  TP={tp} FP={fp} FN={fn}")

    micro_p = total_tp / (total_tp + total_fp) if total_tp + total_fp else 0.0
    micro_r = total_tp / (total_tp + total_fn) if total_tp + total_fn else 0.0
    micro_f1 = 2 * micro_p * micro_r / (micro_p + micro_r) if micro_p + micro_r else 0.0

    lines.append("")
    lines.append(f"MICRO        P={micro_p:.3f} R={micro_r:.3f} F1={micro_f1:.3f}  TP={total_tp} FP={total_fp} FN={total_fn}")

    return "\n".join(lines)

def main():
    golds, preds = read_labels(INPUT_FILE)
    report = compute_token_metrics(golds, preds)

    print(report)
    REPORT_FILE.write_text(report + "\n", encoding="utf-8")
    print(f"\nSaved report to {REPORT_FILE}")

if __name__ == "__main__":
    main()
