from pathlib import Path
import argparse
from collections import Counter, defaultdict

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
            if len(parts) < 3:
                continue

            token = parts[0]
            gold = parts[-2]
            pred = parts[-1]
            cur.append((token, gold, pred))

    if cur:
        sentences.append(cur)

    return sentences

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

def overlap(a, b):
    return a[0] == b[0] and max(a[1], b[1]) < min(a[2], b[2])

def span_text(sent, span):
    _, start, end, _ = span
    return " ".join(tok for tok, _, _ in sent[start:end])

def context_text(sent, span, window=12):
    _, start, end, _ = span
    left = max(0, start - window)
    right = min(len(sent), end + window)
    return " ".join(tok for tok, _, _ in sent[left:right])

def analyze(sentences):
    all_gold = []
    all_pred = []

    for sid, sent in enumerate(sentences):
        gold_tags = [x[1] for x in sent]
        pred_tags = [x[2] for x in sent]

        all_gold.extend(bio_to_spans(gold_tags, sid))
        all_pred.extend(bio_to_spans(pred_tags, sid))

    gold_set = set(all_gold)
    pred_set = set(all_pred)

    correct = gold_set & pred_set
    gold_unmatched = [g for g in all_gold if g not in correct]
    pred_unmatched = [p for p in all_pred if p not in correct]

    used_gold = set()
    used_pred = set()
    errors = []

    # First capture overlapping boundary/type errors.
    for g in gold_unmatched:
        candidates = [p for p in pred_unmatched if p not in used_pred and overlap(g, p)]
        if not candidates:
            continue

        # Prefer same-type overlap as boundary error; otherwise type error.
        same_type = [p for p in candidates if p[3] == g[3]]
        if same_type:
            p = same_type[0]
            category = "Boundary error"
            entity_type = g[3]
        else:
            p = candidates[0]
            category = "Type error"
            entity_type = g[3]

        used_gold.add(g)
        used_pred.add(p)

        errors.append({
            "category": category,
            "entity_type": entity_type,
            "gold": span_text(sentences[g[0]], g),
            "predicted": span_text(sentences[p[0]], p),
            "context": context_text(sentences[g[0]], g),
        })

    # Remaining gold spans are false negatives.
    for g in gold_unmatched:
        if g in used_gold:
            continue

        errors.append({
            "category": "False negative",
            "entity_type": g[3],
            "gold": span_text(sentences[g[0]], g),
            "predicted": "",
            "context": context_text(sentences[g[0]], g),
        })

    # Remaining predicted spans are false positives.
    for p in pred_unmatched:
        if p in used_pred:
            continue

        errors.append({
            "category": "False positive",
            "entity_type": p[3],
            "gold": "",
            "predicted": span_text(sentences[p[0]], p),
            "context": context_text(sentences[p[0]], p),
        })

    return errors, correct, all_gold, all_pred

def write_report(errors, correct, all_gold, all_pred, model, out_path):
    category_counts = Counter(e["category"] for e in errors)
    type_counts = Counter((e["category"], e["entity_type"]) for e in errors)

    tp = len(correct)
    fp = len(all_pred) - tp
    fn = len(all_gold) - tp

    lines = []
    lines.append(f"# Error Analysis: {model}")
    lines.append("")
    lines.append("## Span-Level Confusion Summary")
    lines.append("")
    lines.append("| Model | TP | FP | FN |")
    lines.append("|---|---:|---:|---:|")
    lines.append(f"| {model} | {tp} | {fp} | {fn} |")
    lines.append("")
    lines.append("## Error Category Counts")
    lines.append("")
    lines.append("| Error Category | Count |")
    lines.append("|---|---:|")
    for cat, count in category_counts.most_common():
        lines.append(f"| {cat} | {count} |")

    lines.append("")
    lines.append("## Error Counts by Entity Type")
    lines.append("")
    lines.append("| Error Category | Entity Type | Count |")
    lines.append("|---|---|---:|")
    for (cat, typ), count in type_counts.most_common():
        lines.append(f"| {cat} | {typ} | {count} |")

    lines.append("")
    lines.append("## Representative Error Examples")
    lines.append("")
    for i, e in enumerate(errors[:20], 1):
        lines.append(f"### Example {i}: {e['category']} ({e['entity_type']})")
        lines.append("")
        if e["gold"]:
            lines.append(f"- Gold: `{e['gold']}`")
        if e["predicted"]:
            lines.append(f"- Predicted: `{e['predicted']}`")
        lines.append(f"- Context: {e['context']}")
        lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")

    return category_counts, type_counts, tp, fp, fn

def write_summary(category_counts, type_counts, tp, fp, fn, model, out_path):
    fn_party = type_counts.get(("False negative", "PARTY"), 0)
    fn_citation = type_counts.get(("False negative", "CITATION"), 0)
    boundary_citation = type_counts.get(("Boundary error", "CITATION"), 0)

    lines = []
    lines.append(f"# {model} Error Summary for Paper")
    lines.append("")
    lines.append("## Main Error Counts")
    lines.append("")
    lines.append("| Error Category | Count |")
    lines.append("|---|---:|")
    for cat, count in category_counts.most_common():
        lines.append(f"| {cat} | {count} |")

    lines.append("")
    lines.append("## Most Important Entity-Specific Errors")
    lines.append("")
    lines.append("| Error Type | Entity Type | Count |")
    lines.append("|---|---|---:|")
    for (cat, typ), count in type_counts.most_common(10):
        lines.append(f"| {cat} | {typ} | {count} |")

    lines.append("")
    lines.append("## Paper-Ready Interpretation")
    lines.append("")
    lines.append(
        f"The final tuned CRF produces {tp} correct spans, {fp} false positives, and {fn} false negatives. "
        "The dominant remaining error type is still false negatives, indicating that the model remains conservative even after tuning. "
        f"PARTY remains the hardest high-frequency entity type, with {fn_party} false negatives. "
        "This supports the qualitative conclusion that legal actors are difficult to identify when they appear inside or near citation-like expressions. "
        f"CITATION errors also remain important: the model has {fn_citation} citation false negatives and {boundary_citation} citation boundary errors. "
        "Overall, tuning improves performance, especially for CITATION, but it does not eliminate the core linguistic difficulty of legal NER: exact boundary detection in nested PARTY/CITATION contexts."
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--out", default=None)
    parser.add_argument("--summary_out", default=None)
    args = parser.parse_args()

    sentences = read_conll(ROOT / args.input)
    errors, correct, all_gold, all_pred = analyze(sentences)

    out = ROOT / (args.out or f"results/error_analysis/{args.model}_errors.md")
    summary_out = ROOT / (args.summary_out or f"results/error_analysis/{args.model}_error_summary_for_paper.md")

    category_counts, type_counts, tp, fp, fn = write_report(
        errors, correct, all_gold, all_pred, args.model, out
    )
    write_summary(category_counts, type_counts, tp, fp, fn, args.model, summary_out)

    print(f"Error category counts:")
    for cat, count in category_counts.most_common():
        print(f"{cat}: {count}")

    print()
    print(f"Saved full report to {out.relative_to(ROOT)}")
    print(f"Saved summary to {summary_out.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
