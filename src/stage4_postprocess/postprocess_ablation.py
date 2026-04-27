from pathlib import Path
import subprocess
import sys

from src.stage4_postprocess.postprocess import (
    read_conll,
    write_conll,
    clone_sentences,
    repair_bio_tags,
    tags_to_spans,
    spans_to_tags,
    complete_spans_for_sentence,
    resolve_nested_and_overlaps,
    collect_type_consistency_map,
    apply_type_consistency,
    count_tag_differences,
)

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data/splits/test_crf_pred.conll"
OUT_DIR = ROOT / "data/splits"
RESULTS_DIR = ROOT / "results"


def apply_bio_only(sentences):
    before = clone_sentences(sentences)
    stats = {"bio_repairs": 0, "tag_changes_total": 0}

    for sent in sentences:
        tags = [x["pred"] for x in sent]
        repaired, changes = repair_bio_tags(tags)
        stats["bio_repairs"] += changes

        for item, tag in zip(sent, repaired):
            item["pred"] = tag

    stats["tag_changes_total"] = count_tag_differences(before, sentences)
    return sentences, stats


def apply_span_completion_only(sentences):
    """
    Isolates span completion as much as possible.
    We also resolve overlaps because flat BIO cannot represent overlapping spans.
    """
    before = clone_sentences(sentences)
    stats = {
        "bio_repairs": 0,
        "span_completions": 0,
        "nested_overlap_resolutions": 0,
        "tag_changes_total": 0,
    }

    for sent in sentences:
        spans, bio_changes, completion_changes = complete_spans_for_sentence(sent)
        spans, nested_removed = resolve_nested_and_overlaps(spans)
        tags = spans_to_tags(len(sent), spans)

        for item, tag in zip(sent, tags):
            item["pred"] = tag

        stats["bio_repairs"] += bio_changes
        stats["span_completions"] += completion_changes
        stats["nested_overlap_resolutions"] += nested_removed

    stats["tag_changes_total"] = count_tag_differences(before, sentences)
    return sentences, stats


def apply_nested_only(sentences):
    before = clone_sentences(sentences)
    stats = {"nested_overlap_resolutions": 0, "tag_changes_total": 0}

    for sent in sentences:
        spans = tags_to_spans([x["pred"] for x in sent])
        spans, removed = resolve_nested_and_overlaps(spans)
        tags = spans_to_tags(len(sent), spans)

        for item, tag in zip(sent, tags):
            item["pred"] = tag

        stats["nested_overlap_resolutions"] += removed

    stats["tag_changes_total"] = count_tag_differences(before, sentences)
    return sentences, stats


def apply_type_consistency_only(sentences):
    before = clone_sentences(sentences)
    mapping = collect_type_consistency_map(sentences)
    changes = apply_type_consistency(sentences, mapping)

    stats = {
        "type_consistency_mappings": len(mapping),
        "type_consistency_changes": changes,
        "tag_changes_total": count_tag_differences(before, sentences),
    }
    return sentences, stats


def run_eval(pred_path, model_name):
    cmd = [
        sys.executable,
        "-m",
        "src.evaluation.span_eval",
        "--input",
        str(pred_path.relative_to(ROOT)),
        "--model",
        model_name,
    ]

    result = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("[stderr]")
        print(result.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"Evaluation failed for {model_name}")

    return result.stdout


def extract_overall(stdout):
    """
    Extract the first markdown result row after the header.
    Expected row:
    | Model | Precision | Recall | F1 | TP | FP | FN |
    """
    for line in stdout.splitlines():
        if line.startswith("| CRF_"):
            parts = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(parts) >= 7:
                return {
                    "model": parts[0],
                    "precision": parts[1],
                    "recall": parts[2],
                    "f1": parts[3],
                    "tp": parts[4],
                    "fp": parts[5],
                    "fn": parts[6],
                }
    return None


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    experiments = [
        ("bio_only", "CRF_Post_BIOOnly", apply_bio_only),
        ("span_completion_only", "CRF_Post_SpanCompletionOnly", apply_span_completion_only),
        ("nested_only", "CRF_Post_NestedOnly", apply_nested_only),
        ("type_consistency_only", "CRF_Post_TypeConsistencyOnly", apply_type_consistency_only),
    ]

    rows = []
    detail_lines = []
    detail_lines.append("# Stage 4 Post-processing Ablation")
    detail_lines.append("")
    detail_lines.append("This experiment isolates the effect of each Stage 4 post-processing component on the CRF test predictions.")
    detail_lines.append("")

    for short_name, model_name, fn in experiments:
        print("\n" + "=" * 80)
        print(f"Running Stage 4 ablation: {model_name}")
        print("=" * 80)

        sentences = read_conll(INPUT)
        processed, stats = fn(sentences)

        out_path = OUT_DIR / f"test_crf_{short_name}_pred.conll"
        write_conll(processed, out_path)

        print(f"Wrote {out_path.relative_to(ROOT)}")
        print("Stats:")
        for k, v in stats.items():
            print(f"- {k}: {v}")

        stdout = run_eval(out_path, model_name)
        overall = extract_overall(stdout)

        if overall:
            rows.append((short_name, model_name, stats, overall))

        detail_lines.append(f"## {model_name}")
        detail_lines.append("")
        detail_lines.append("### Operation Statistics")
        detail_lines.append("")
        detail_lines.append("| Operation | Count |")
        detail_lines.append("|---|---:|")
        for k, v in stats.items():
            detail_lines.append(f"| {k} | {v} |")
        detail_lines.append("")

        if overall:
            detail_lines.append("### Overall Span-Level Result")
            detail_lines.append("")
            detail_lines.append("| Model | Precision | Recall | F1 | TP | FP | FN |")
            detail_lines.append("|---|---:|---:|---:|---:|---:|---:|")
            detail_lines.append(
                f"| {overall['model']} | {overall['precision']} | {overall['recall']} | {overall['f1']} | "
                f"{overall['tp']} | {overall['fp']} | {overall['fn']} |"
            )
            detail_lines.append("")

    summary_lines = []
    summary_lines.append("# Stage 4 Post-processing Ablation Summary")
    summary_lines.append("")
    summary_lines.append("Baseline CRF span-level result: Precision = 0.781, Recall = 0.418, F1 = 0.545.")
    summary_lines.append("")
    summary_lines.append("| System | Precision | Recall | F1 | TP | FP | FN | Main Tag Changes |")
    summary_lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")

    summary_lines.append("| CRF baseline | 0.781 | 0.418 | 0.545 | 82 | 23 | 114 | 0 |")

    for short_name, model_name, stats, overall in rows:
        tag_changes = stats.get("tag_changes_total", 0)
        summary_lines.append(
            f"| {model_name} | {overall['precision']} | {overall['recall']} | {overall['f1']} | "
            f"{overall['tp']} | {overall['fp']} | {overall['fn']} | {tag_changes} |"
        )

    summary_lines.append("")
    summary_lines.append("## Interpretation Template")
    summary_lines.append("")
    summary_lines.append("Use this table to identify which Stage 4 component changes performance.")
    summary_lines.append("If span-completion-only lowers F1 substantially, then the full post-processing degradation is mainly caused by over-expanding entity boundaries.")
    summary_lines.append("If type-consistency-only changes little, then repeated-string voting is not a major source of either improvement or harm in this test set.")
    summary_lines.append("If nested-only changes little, then the current CRF predictions rarely contain overlapping spans that need resolution.")
    summary_lines.append("")

    (RESULTS_DIR / "postprocess_ablation.md").write_text("\n".join(detail_lines), encoding="utf-8")
    (RESULTS_DIR / "postprocess_ablation_summary.md").write_text("\n".join(summary_lines), encoding="utf-8")

    print("\nSaved results/postprocess_ablation.md")
    print("Saved results/postprocess_ablation_summary.md")


if __name__ == "__main__":
    main()
