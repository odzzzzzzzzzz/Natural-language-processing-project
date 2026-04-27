from pathlib import Path
import argparse
from collections import Counter, defaultdict

ENTITY_PRIORITY = {
    "CITATION": 7,
    "STATUTE": 6,
    "COURT": 5,
    "JUDGE": 4,
    "ORG": 3,
    "PARTY": 2,
    "DATE": 1,
}

CORPORATE_SUFFIXES = {
    "inc", "inc.", "co", "co.", "corp", "corp.", "corporation",
    "company", "ltd", "ltd.", "llc", "association"
}

COURT_CONTINUATIONS = {
    "of", "appeals", "for", "the", "district", "circuit",
    "southern", "northern", "eastern", "western", "united", "states"
}

CITATION_CONTINUATIONS = {
    ",", ".", "(", ")", "-", "–", "—",
    "U", "S", "F", "Supp", "Ct", "L", "Ed",
    "No", "Nos", "at", "p", "pp", "v", "supra", "id"
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
            if len(parts) >= 3:
                token, gold, pred = parts[0], parts[-2], parts[-1]
            elif len(parts) == 2:
                token, gold = parts
                pred = "O"
            else:
                continue

            cur.append({"token": token, "gold": gold, "pred": pred})

    if cur:
        sentences.append(cur)

    return sentences


def write_conll(sentences, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        for sent in sentences:
            for item in sent:
                f.write(f"{item['token']}\t{item['gold']}\t{item['pred']}\n")
            f.write("\n")


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


def span_text(sent, span):
    start, end, _ = span
    return " ".join(item["token"] for item in sent[start:end])


def normalized_span_text(text):
    return (
        " ".join(text.lower().split())
        .replace(" .", ".")
        .replace(" ,", ",")
        .replace("( ", "(")
        .replace(" )", ")")
    )


def is_digit_like(token):
    return any(ch.isdigit() for ch in token)


def looks_like_year(token):
    return token.isdigit() and len(token) == 4


def complete_citation(sent, start, end):
    """
    Conservative span completion for citations.
    Example target:
      379 U . S . 29  -> 379 U . S . 29 , 33 ( 1964 )
    """
    n = len(sent)
    j = end
    steps = 0

    while j < n and steps < 10:
        tok = sent[j]["token"]
        low = tok.lower().strip(".")

        allowed = (
            tok in CITATION_CONTINUATIONS
            or low in CITATION_CONTINUATIONS
            or is_digit_like(tok)
        )

        if not allowed:
            break

        # Avoid swallowing a new sentence after a year.
        if j > end and looks_like_year(sent[j - 1]["token"]) and tok == ".":
            break

        j += 1
        steps += 1

    return start, j


def complete_party(sent, start, end):
    """
    Conservative completion for corporate party names.
    Example:
      Hazeltine Research , Inc -> Hazeltine Research , Inc .
    """
    n = len(sent)
    j = end
    steps = 0

    while j < n and steps < 5:
        tok = sent[j]["token"]
        low = tok.lower()

        if tok == ",":
            j += 1
        elif low in CORPORATE_SUFFIXES:
            j += 1
        elif tok == "." and j > start and sent[j - 1]["token"].lower().rstrip(".") in CORPORATE_SUFFIXES:
            j += 1
        else:
            break

        steps += 1

    return start, j


def complete_court(sent, start, end):
    """
    Conservative completion for court names.
    Example:
      Court -> Court of Appeals
    """
    n = len(sent)
    j = end
    steps = 0

    while j < n and steps < 8:
        low = sent[j]["token"].lower().strip(".")
        if low in COURT_CONTINUATIONS:
            j += 1
            steps += 1
        else:
            break

    return start, j


def repair_bio_tags(tags):
    repaired = []
    prev_prefix = "O"
    prev_type = None
    changes = 0

    for tag in tags:
        prefix, typ = split_tag(tag)

        if prefix == "I" and (prev_prefix == "O" or prev_type != typ):
            repaired.append(f"B-{typ}")
            changes += 1
            prev_prefix, prev_type = "B", typ
        elif prefix == "O":
            repaired.append("O")
            prev_prefix, prev_type = "O", None
        else:
            repaired.append(tag)
            prev_prefix, prev_type = prefix, typ

    return repaired, changes


def complete_spans_for_sentence(sent):
    old_tags = [x["pred"] for x in sent]
    repaired_tags, bio_changes = repair_bio_tags(old_tags)
    spans = tags_to_spans(repaired_tags)

    new_spans = []
    completion_changes = 0

    for start, end, typ in spans:
        old = (start, end)

        if typ == "CITATION":
            start, end = complete_citation(sent, start, end)
        elif typ == "PARTY":
            start, end = complete_party(sent, start, end)
        elif typ == "COURT":
            start, end = complete_court(sent, start, end)

        if (start, end) != old:
            completion_changes += 1

        new_spans.append([start, end, typ])

    return new_spans, bio_changes, completion_changes


def spans_overlap(a, b):
    return max(a[0], b[0]) < min(a[1], b[1])


def resolve_nested_and_overlaps(spans):
    """
    Flat BIO cannot keep nested entities.
    We keep the higher-priority span. If priorities tie, keep the longer span.
    """
    spans = sorted(
        spans,
        key=lambda sp: (sp[0], -(sp[1] - sp[0]), -ENTITY_PRIORITY.get(sp[2], 0))
    )

    kept = []
    removed = 0

    for sp in spans:
        conflicts = [i for i, old in enumerate(kept) if spans_overlap(sp, old)]

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


def collect_type_consistency_map(sentences):
    """
    If the same predicted span string appears at least 3 times, and one type
    dominates by at least 3x, use that type consistently.
    """
    counts = defaultdict(Counter)

    for sent in sentences:
        spans = tags_to_spans([x["pred"] for x in sent])
        for sp in spans:
            text = normalized_span_text(span_text(sent, sp))
            if len(text) < 3:
                continue
            counts[text][sp[2]] += 1

    mapping = {}

    for text, counter in counts.items():
        total = sum(counter.values())
        if total < 3:
            continue

        common = counter.most_common()
        best_type, best_count = common[0]
        second_count = common[1][1] if len(common) > 1 else 0

        if best_count >= 3 and best_count >= 3 * max(1, second_count):
            mapping[text] = best_type

    return mapping


def apply_type_consistency(sentences, mapping):
    changes = 0

    for sent in sentences:
        spans = tags_to_spans([x["pred"] for x in sent])
        changed = False

        for sp in spans:
            text = normalized_span_text(span_text(sent, sp))
            if text in mapping and sp[2] != mapping[text]:
                sp[2] = mapping[text]
                changes += 1
                changed = True

        if changed:
            spans, _ = resolve_nested_and_overlaps(spans)
            tags = spans_to_tags(len(sent), spans)
            for item, tag in zip(sent, tags):
                item["pred"] = tag

    return changes


def count_tag_differences(before_sentences, after_sentences):
    diff = 0
    for before, after in zip(before_sentences, after_sentences):
        for b, a in zip(before, after):
            if b["pred"] != a["pred"]:
                diff += 1
    return diff


def clone_sentences(sentences):
    return [[dict(item) for item in sent] for sent in sentences]


def full_postprocess(sentences):
    before = clone_sentences(sentences)

    stats = {
        "bio_repairs": 0,
        "span_completions": 0,
        "nested_overlap_resolutions": 0,
        "type_consistency_changes": 0,
        "type_consistency_mappings": 0,
        "tag_changes_total": 0,
    }

    # Step 1: BIO repair + span completion + nested/overlap resolution.
    for sent in sentences:
        spans, bio_changes, completion_changes = complete_spans_for_sentence(sent)
        spans, nested_removed = resolve_nested_and_overlaps(spans)
        tags = spans_to_tags(len(sent), spans)

        for item, tag in zip(sent, tags):
            item["pred"] = tag

        stats["bio_repairs"] += bio_changes
        stats["span_completions"] += completion_changes
        stats["nested_overlap_resolutions"] += nested_removed

    # Step 2: document-level type consistency.
    mapping = collect_type_consistency_map(sentences)
    stats["type_consistency_mappings"] = len(mapping)
    stats["type_consistency_changes"] = apply_type_consistency(sentences, mapping)

    # Step 3: final overlap cleanup.
    for sent in sentences:
        spans = tags_to_spans([x["pred"] for x in sent])
        spans, nested_removed = resolve_nested_and_overlaps(spans)
        tags = spans_to_tags(len(sent), spans)

        for item, tag in zip(sent, tags):
            item["pred"] = tag

        stats["nested_overlap_resolutions"] += nested_removed

    stats["tag_changes_total"] = count_tag_differences(before, sentences)

    return sentences, stats, mapping


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/splits/test_crf_pred.conll")
    parser.add_argument("--output", default="data/splits/test_crf_full_postprocess_pred.conll")
    args = parser.parse_args()

    sentences = read_conll(args.input)
    sentences, stats, mapping = full_postprocess(sentences)
    write_conll(sentences, args.output)

    print(f"Read: {args.input}")
    print(f"Wrote: {args.output}")
    print()
    print("Post-processing statistics:")
    for key, value in stats.items():
        print(f"- {key}: {value}")

    if mapping:
        print()
        print("First type-consistency mappings:")
        for i, (text, typ) in enumerate(mapping.items()):
            if i >= 10:
                break
            print(f"  {text!r} -> {typ}")


if __name__ == "__main__":
    main()
