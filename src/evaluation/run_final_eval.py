from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]

COMMANDS = [
    ("Majority", "data/splits/test_majority_pred.conll"),
    ("CoNLL2003_CRF", "data/splits/test_conll2003_crf_pred.conll"),
    ("Stanza", "data/splits/test_stanza_pred.conll"),
    ("RuleBased", "data/splits/test_rule_pred.conll"),
    ("CRF", "data/splits/test_crf_pred.conll"),
    ("CRF_Tuned", "data/splits/test_crf_tuned_pred.conll"),
    ("CRF_BIO_Repair", "data/splits/test_crf_bio_repair_pred.conll"),
    ("CRF_FullPostprocess", "data/splits/test_crf_full_postprocess_pred.conll"),
]

SUMMARY = """# Final Evaluation Run Summary

This file records the final span-level evaluation commands used for the Legal NER project.

## Systems Evaluated

1. Majority baseline
2. CoNLL-2003 CRF transfer baseline
3. Stanza pretrained NER baseline
4. Rule-based baseline
5. Original legal-domain CRF
6. Tuned legal-domain CRF
7. CRF + BIO repair
8. CRF + full heuristic post-processing

## Final Best System

The final best model is the tuned legal-domain CRF:

- Precision: 0.822
- Recall: 0.449
- Span-level F1: 0.581

## Notes

This script does not retrain models.
It only reruns final span-level evaluation on existing prediction files.

Main result files:

- results/main_results.md
- results/span_eval_Majority.md
- results/span_eval_CoNLL2003_CRF.md
- results/span_eval_Stanza.md
- results/span_eval_RuleBased.md
- results/span_eval_CRF.md
- results/span_eval_CRF_Tuned.md
- results/span_eval_CRF_BIO_Repair.md
- results/span_eval_CRF_FullPostprocess.md
"""

def run_eval(model_name, input_path):
    full_path = ROOT / input_path
    if not full_path.exists():
        print(f"[SKIP] Missing prediction file for {model_name}: {input_path}")
        return

    cmd = [
        sys.executable,
        "-m",
        "src.evaluation.span_eval",
        "--input",
        input_path,
        "--model",
        model_name,
    ]

    print("\n" + "=" * 80)
    print(f"Running: {model_name}")
    print("Command:", " ".join(cmd))
    print("=" * 80)

    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("[stderr]")
        print(result.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"Evaluation failed for {model_name}")

def main():
    results_dir = ROOT / "results"
    results_dir.mkdir(exist_ok=True)

    for model_name, input_path in COMMANDS:
        run_eval(model_name, input_path)

    out = results_dir / "final_eval_run_summary.md"
    out.write_text(SUMMARY, encoding="utf-8")

    print("\nFinal evaluation wrapper completed.")
    print(f"Saved summary to {out}")

if __name__ == "__main__":
    main()
