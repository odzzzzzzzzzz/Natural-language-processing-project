from pathlib import Path
import argparse
import csv
import random
import statistics

from src.stage3_crf.tune_crf import (
    ROOT,
    read_conll,
    sent2features,
    sent2labels,
    train_crf,
    span_f1,
)

def run_one_setting(train_pool, test_sents, fraction, seed, c1, c2, max_iterations):
    rng = random.Random(seed)
    indices = list(range(len(train_pool)))
    rng.shuffle(indices)

    n_train = max(1, int(round(len(train_pool) * fraction)))
    selected = [train_pool[i] for i in indices[:n_train]]

    X_train = [sent2features(s) for s in selected]
    y_train = [sent2labels(s) for s in selected]

    X_test = [sent2features(s) for s in test_sents]
    y_test = [sent2labels(s) for s in test_sents]

    crf = train_crf(
        X_train,
        y_train,
        c1=c1,
        c2=c2,
        max_iterations=max_iterations,
    )

    y_pred = crf.predict(X_test)
    p, r, f1, tp, fp, fn = span_f1(y_test, y_pred)

    return {
        "fraction": fraction,
        "seed": seed,
        "n_train": n_train,
        "precision": p,
        "recall": r,
        "f1": f1,
        "tp": tp,
        "fp": fp,
        "fn": fn,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", default="data/splits/train.conll")
    parser.add_argument("--dev", default="data/splits/dev.conll")
    parser.add_argument("--test", default="data/splits/test.conll")
    parser.add_argument("--out_csv", default="results/learning_curve.csv")
    parser.add_argument("--out_md", default="results/learning_curve_summary.md")
    parser.add_argument("--c1", type=float, default=0.01)
    parser.add_argument("--c2", type=float, default=0.1)
    parser.add_argument("--max_iterations", type=int, default=100)
    args = parser.parse_args()

    train_sents = read_conll(ROOT / args.train)
    dev_sents = read_conll(ROOT / args.dev)
    test_sents = read_conll(ROOT / args.test)

    train_pool = train_sents + dev_sents

    fractions = [0.25, 0.50, 0.75, 1.00]
    seeds = [13, 21, 42]

    print(f"Train sentences: {len(train_sents)}")
    print(f"Dev sentences: {len(dev_sents)}")
    print(f"Train+Dev pool: {len(train_pool)}")
    print(f"Test sentences: {len(test_sents)}")
    print(f"CRF params: c1={args.c1}, c2={args.c2}")
    print("Running learning curve experiment...")

    rows = []

    for fraction in fractions:
        for seed in seeds:
            print(f"\nTraining fraction={fraction:.2f}, seed={seed}")
            row = run_one_setting(
                train_pool=train_pool,
                test_sents=test_sents,
                fraction=fraction,
                seed=seed,
                c1=args.c1,
                c2=args.c2,
                max_iterations=args.max_iterations,
            )
            rows.append(row)
            print(
                f"n_train={row['n_train']} "
                f"P={row['precision']:.3f} "
                f"R={row['recall']:.3f} "
                f"F1={row['f1']:.3f} "
                f"TP={row['tp']} FP={row['fp']} FN={row['fn']}"
            )

    out_csv = ROOT / args.out_csv
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "fraction",
                "seed",
                "n_train",
                "precision",
                "recall",
                "f1",
                "tp",
                "fp",
                "fn",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    grouped = {}
    for row in rows:
        grouped.setdefault(row["fraction"], []).append(row)

    lines = []
    lines.append("# Learning Curve / Annotation Size Experiment")
    lines.append("")
    lines.append("## Motivation")
    lines.append("")
    lines.append("This experiment tests whether adding more annotated training data improves legal NER performance.")
    lines.append("We train the same tuned CRF architecture on different fractions of the train+dev pool and evaluate each model on the same held-out test set.")
    lines.append("")
    lines.append("The CRF parameters are fixed to the final dev-selected tuned setting:")
    lines.append("")
    lines.append("| c1 | c2 |")
    lines.append("|---:|---:|")
    lines.append(f"| {args.c1} | {args.c2} |")
    lines.append("")
    lines.append("Each fraction is repeated with three random seeds.")
    lines.append("")
    lines.append("## Summary Results")
    lines.append("")
    lines.append("| Training Fraction | Mean Train Units | Mean Precision | Mean Recall | Mean Span F1 | F1 Std |")
    lines.append("|---:|---:|---:|---:|---:|---:|")

    for fraction in sorted(grouped):
        group = grouped[fraction]
        mean_n = statistics.mean(r["n_train"] for r in group)
        mean_p = statistics.mean(r["precision"] for r in group)
        mean_r = statistics.mean(r["recall"] for r in group)
        mean_f1 = statistics.mean(r["f1"] for r in group)
        std_f1 = statistics.stdev(r["f1"] for r in group) if len(group) > 1 else 0.0

        lines.append(
            f"| {fraction:.2f} | {mean_n:.1f} | {mean_p:.3f} | {mean_r:.3f} | {mean_f1:.3f} | {std_f1:.3f} |"
        )

    lines.append("")
    lines.append("## Individual Runs")
    lines.append("")
    lines.append("| Fraction | Seed | Train Units | Precision | Recall | F1 | TP | FP | FN |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|")

    for row in rows:
        lines.append(
            f"| {row['fraction']:.2f} | {row['seed']} | {row['n_train']} | "
            f"{row['precision']:.3f} | {row['recall']:.3f} | {row['f1']:.3f} | "
            f"{row['tp']} | {row['fp']} | {row['fn']} |"
        )

    full_group = grouped[1.00]
    full_mean = statistics.mean(r["f1"] for r in full_group)
    small_group = grouped[0.25]
    small_mean = statistics.mean(r["f1"] for r in small_group)

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        f"The 25% training condition achieves mean span F1 of {small_mean:.3f}, while the 100% training condition achieves mean span F1 of {full_mean:.3f}. "
        "This learning-curve experiment shows whether the model benefits from additional annotated data under a controlled held-out test setup."
    )
    lines.append("")
    lines.append("Because this is a pilot-scale dataset, random variation across sampled subsets is expected. The key trend to report is whether performance generally improves as more annotated training passages are used.")
    lines.append("")
    lines.append("## Paper-Ready Paragraph")
    lines.append("")
    lines.append(
        "To test the effect of annotation size, we ran a learning-curve experiment using the tuned CRF architecture. "
        "We trained models on 25%, 50%, 75%, and 100% of the train plus development pool, repeating each condition with three random seeds and evaluating all models on the same held-out test set. "
        "This experiment measures whether additional in-domain legal annotation improves strict span-level NER performance and helps distinguish data scarcity from feature-engineering limitations."
    )

    out_md = ROOT / args.out_md
    out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nSaved CSV to {out_csv}")
    print(f"Saved summary to {out_md}")

if __name__ == "__main__":
    main()
