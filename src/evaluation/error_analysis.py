from pathlib import Path
from collections import defaultdict, Counter

INPUT_FILE = Path("data/splits/test_crf_pred.conll")
OUT_MD = Path("results/error_analysis.md")

def entity_type(tag):
    if tag == "O":
        return "O"
    return tag.split("-", 1)[1]

def read_tokens(path):
    toks = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            toks.append(("", "", ""))
            continue
        token, gold, pred = line.split("\t")
        toks.append((token, gold, pred))
    return toks

def context(tokens, idx, window=7):
    start = max(0, idx - window)
    end = min(len(tokens), idx + window + 1)
    words = []
    for j in range(start, end):
        tok, gold, pred = tokens[j]
        if not tok:
            continue
        if j == idx:
            words.append(f"[{tok}]")
        else:
            words.append(tok)
    return " ".join(words)

def classify_error(token, gold, pred):
    gt = entity_type(gold)
    pt = entity_type(pred)

    if gold == "O" and pred != "O":
        return "False positive"
    if gold != "O" and pred == "O":
        return "False negative"
    if gt != pt:
        return "Wrong type"
    if gold != pred:
        return "BIO boundary error"
    return "Correct"

def main():
    tokens = read_tokens(INPUT_FILE)

    error_counts = Counter()
    by_type = defaultdict(Counter)
    examples = defaultdict(list)

    for i, (tok, gold, pred) in enumerate(tokens):
        if not tok:
            continue
        err = classify_error(tok, gold, pred)
        if err == "Correct":
            continue

        gt = entity_type(gold)
        pt = entity_type(pred)
        key_type = gt if gt != "O" else pt

        error_counts[err] += 1
        by_type[key_type][err] += 1

        if len(examples[(key_type, err)]) < 5:
            examples[(key_type, err)].append({
                "token": tok,
                "gold": gold,
                "pred": pred,
                "context": context(tokens, i),
            })

    lines = []
    lines.append("# Error Analysis for CRF Test Predictions")
    lines.append("")
    lines.append("## Error counts")
    for err, count in error_counts.most_common():
        lines.append(f"- {err}: {count}")

    lines.append("")
    lines.append("## Error counts by entity type")
    for typ in sorted(by_type):
        lines.append(f"\n### {typ}")
        for err, count in by_type[typ].most_common():
            lines.append(f"- {err}: {count}")

    lines.append("")
    lines.append("## Representative examples")
    for (typ, err), exs in sorted(examples.items()):
        lines.append(f"\n### {typ} — {err}")
        for ex in exs:
            lines.append(f"- Token: `{ex['token']}` | Gold: `{ex['gold']}` | Pred: `{ex['pred']}`")
            lines.append(f"  - Context: {ex['context']}")

    lines.append("")
    lines.append("## Interpretation")
    lines.append(
        "The dominant error type is false negatives, meaning the CRF often leaves gold entities unlabeled. "
        "This is consistent with the small annotated dataset and the skew toward CITATION entities. "
        "ORG remains especially difficult because it appears less frequently and has more variable surface forms. "
        "Some errors are BIO boundary errors, especially around legal citations split by punctuation or reporter abbreviations. "
        "The paragraph-similarity analysis also suggests that citation fragments sometimes span adjacent text chunks, which can hurt recall."
    )

    md = "\n".join(lines)
    OUT_MD.write_text(md + "\n", encoding="utf-8")
    print(md)
    print(f"\nSaved {OUT_MD}")

if __name__ == "__main__":
    main()
