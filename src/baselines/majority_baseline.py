from pathlib import Path
from collections import Counter

INPUT_FILE = Path("data/splits/test.conll")
OUTPUT_FILE = Path("data/splits/test_majority_pred.conll")
REPORT_FILE = Path("results/majority_baseline_report.txt")

def entity_type(tag):
    if tag == "O":
        return "O"
    return tag.split("-", 1)[1]

def main():
    golds = []
    preds = []

    with INPUT_FILE.open("r", encoding="utf-8") as f, OUTPUT_FILE.open("w", encoding="utf-8") as out:
        for line in f:
            if not line.strip():
                out.write("\n")
                continue
            parts = line.rstrip("\n").split("\t")
            tok, gold = parts[0], parts[1]
            pred = "O"
            golds.append(gold)
            preds.append(pred)
            out.write(f"{tok}\t{gold}\t{pred}\n")

    labels = sorted(set(entity_type(x) for x in golds if x != "O"))

    total_tp = total_fp = total_fn = 0
    lines = ["# Majority Baseline Report", ""]

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

        P = tp/(tp+fp) if tp+fp else 0
        R = tp/(tp+fn) if tp+fn else 0
        F1 = 2*P*R/(P+R) if P+R else 0

        lines.append(f"{lab:10s} P={P:.3f} R={R:.3f} F1={F1:.3f} TP={tp} FP={fp} FN={fn}")

    micro_p = total_tp/(total_tp+total_fp) if total_tp+total_fp else 0
    micro_r = total_tp/(total_tp+total_fn) if total_tp+total_fn else 0
    micro_f1 = 2*micro_p*micro_r/(micro_p+micro_r) if micro_p+micro_r else 0

    lines.append("")
    lines.append(f"MICRO P={micro_p:.3f} R={micro_r:.3f} F1={micro_f1:.3f}")

    report = "\n".join(lines)
    print(report)
    REPORT_FILE.write_text(report + "\n", encoding="utf-8")
    print(f"\nSaved predictions to {OUTPUT_FILE}")
    print(f"Saved report to {REPORT_FILE}")

if __name__ == "__main__":
    main()
