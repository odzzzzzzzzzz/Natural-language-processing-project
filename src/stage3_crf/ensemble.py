from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[2]

HIGH_PRECISION_RULE_TYPES = {"CITATION", "STATUTE", "DATE"}

ENTITY_PRIORITY = {
    "CITATION": 7,
    "STATUTE": 6,
    "COURT": 5,
    "JUDGE": 4,
    "DATE": 3,
    "ORG": 2,
    "PARTY": 1,
}

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

def read_pred_file(path):
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
            if len(parts) >= 3:
                token, gold, pred = parts[0], parts[-2], parts[-1]
            elif len(parts) == 2:
                token, gold = parts
                pred = "O"
            else:
                continue

            cur.append({
                "token": token,
                "gold": gold,
                "pred": pred,
            })

    if cur:
        sentences.append(cur)

    return sentences

def tags_to_spans(tags):
    spans = []
    start = None
    cur_type = None

    for i, tag in enumerate(tags):
        prefix, typ = split_tag(tag)

        if prefix == "O":
            if cur_type is not None:
                spans.append([start, i, cur_type])
                start = None
                cur_type = None
            continue

        if prefix == "B":
            if cur_type is not None:
                spans.append([start, i, cur_type])
            start = i
            cur_type = typ
            continue

        if prefix == "I":
            if cur_type is None:
                start = i
                cur_type = typ
            elif typ != cur_type:
                spans.append([start, i, cur_type])
                start = i
                cur_type = typ

    if cur_type is not None:
        spans.append([start, len(tags), cur_type])

    return spans

def spans_to_tags(n, spans):
    tags = ["O"] * n

    for start, end, typ in spans:
        if start < 0 or end > n or start >= end:
            continue

        tags[start] = f"B-{typ}"
        for i in range(start + 1, end):
            tags[i] = f"I-{typ}"

    return tags

def overlap(a, b):
    return max(a[0], b[0]) < min(a[1], b[1])

def resolve_overlaps(spans):
    """
    If ensemble creates overlapping spans, keep higher-priority entity.
    If priority ties, keep the longer span.
    """
    spans = sorted(
        spans,
        key=lambda sp: (sp[0], -(sp[1] - sp[0]), -ENTITY_PRIORITY.get(sp[2], 0))
    )

    kept = []
    removed = 0

    for sp in spans:
        conflicts = [i for i, old in enumerate(kept) if overlap(sp, old)]

        if not conflicts:
            kept.append(sp)
            continue

        should_add = True

        for idx in sorted(conflicts, reverse=True):
            old = kept[idx]
            old_score = (ENTITY_PRIORITY.get(old[2], 0), old[1] - old[0])
            new_score = (ENTITY_PRIORITY.get(sp[2], 0), sp[1] - sp[0])

            if new_score > old_score:
                kept.pop(idx)
                removed += 1
            else:
                should_add = False
                removed += 1

        if should_add:
            kept.append(sp)

    kept = sorted(kept, key=lambda sp: (sp[0], sp[1]))
    return kept, removed

def same_tokens(a, b):
    if len(a) != len(b):
        return False
    return all(x["token"] == y["token"] and x["gold"] == y["gold"] for x, y in zip(a, b))

def ensemble_sentence(crf_sent, rule_sent):
    if not same_tokens(crf_sent, rule_sent):
        raise ValueError("CRF and rule prediction files do not align.")

    crf_tags = [x["pred"] for x in crf_sent]
    rule_tags = [x["pred"] for x in rule_sent]

    crf_spans = tags_to_spans(crf_tags)
    rule_spans = tags_to_spans(rule_tags)

    final_spans = [list(sp) for sp in crf_spans]

    stats = {
        "rule_spans_seen": 0,
        "rule_spans_added": 0,
        "rule_spans_replaced": 0,
        "rule_spans_skipped": 0,
        "overlap_resolutions": 0,
    }

    for rsp in rule_spans:
        r_start, r_end, r_type = rsp

        if r_type not in HIGH_PRECISION_RULE_TYPES:
            continue

        stats["rule_spans_seen"] += 1

        conflicts = [sp for sp in final_spans if overlap(rsp, sp)]

        # Case 1: CRF missed this high-precision rule span entirely.
        if not conflicts:
            final_spans.append(list(rsp))
            stats["rule_spans_added"] += 1
            continue

        # Case 2: Same type overlap.
        # Keep the CRF span unless rule span is exact or rule type has very high priority.
        same_type = [sp for sp in conflicts if sp[2] == r_type]

        if same_type:
            # If the rule span is exactly one of the CRF spans, nothing to change.
            if any(sp[0] == r_start and sp[1] == r_end and sp[2] == r_type for sp in same_type):
                stats["rule_spans_skipped"] += 1
                continue

            # For DATE and STATUTE, rule spans are often boundary reliable.
            if r_type in {"DATE", "STATUTE"}:
                final_spans = [sp for sp in final_spans if not overlap(rsp, sp)]
                final_spans.append(list(rsp))
                stats["rule_spans_replaced"] += 1
            else:
                stats["rule_spans_skipped"] += 1

            continue

        # Case 3: Different type conflict.
        # Prefer rule only for STATUTE; otherwise keep CRF.
        if r_type == "STATUTE":
            final_spans = [sp for sp in final_spans if not overlap(rsp, sp)]
            final_spans.append(list(rsp))
            stats["rule_spans_replaced"] += 1
        else:
            stats["rule_spans_skipped"] += 1

    final_spans, removed = resolve_overlaps(final_spans)
    stats["overlap_resolutions"] += removed

    tags = spans_to_tags(len(crf_sent), final_spans)
    out_sent = []

    for item, tag in zip(crf_sent, tags):
        out_sent.append({
            "token": item["token"],
            "gold": item["gold"],
            "pred": tag,
        })

    return out_sent, stats

def write_pred(sentences, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        for sent in sentences:
            for item in sent:
                f.write(f"{item['token']}\t{item['gold']}\t{item['pred']}\n")
            f.write("\n")

def add_stats(total, cur):
    for k, v in cur.items():
        total[k] = total.get(k, 0) + v

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--crf", required=True)
    parser.add_argument("--rules", default="data/splits/test_rule_pred.conll")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    crf_sents = read_pred_file(ROOT / args.crf)
    rule_sents = read_pred_file(ROOT / args.rules)

    if len(crf_sents) != len(rule_sents):
        raise ValueError("CRF and rule files have different number of sentences/passages.")

    out_sents = []
    total_stats = {}

    for crf_sent, rule_sent in zip(crf_sents, rule_sents):
        out_sent, stats = ensemble_sentence(crf_sent, rule_sent)
        out_sents.append(out_sent)
        add_stats(total_stats, stats)

    write_pred(out_sents, ROOT / args.output)

    print(f"CRF input: {args.crf}")
    print(f"Rule input: {args.rules}")
    print(f"Output: {args.output}")
    print()
    print("Ensemble statistics:")
    for k, v in total_stats.items():
        print(f"- {k}: {v}")

if __name__ == "__main__":
    main()
