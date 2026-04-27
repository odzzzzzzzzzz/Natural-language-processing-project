import re
from pathlib import Path

INPUT_FILE = Path("data/splits/test.conll")
OUTPUT_FILE = Path("data/splits/test_rule_pred.conll")

CASE_CITATION_RE = re.compile(
    r"([A-Z][A-Za-z.&']+(?:\s+[A-Z][A-Za-z.&']+)*\s+v\s+\.\s+[A-Z][A-Za-z.&']+(?:\s+[A-Z][A-Za-z.&']+)*\s*,?\s+\d+\s+U\s+\.\s*S\s+\.\s+\d+(?:\s*,\s*\d+)?(?:\s*\(\s*\d{4}\s*\))?)"
)

US_CITATION_RE = re.compile(
    r"(\d+\s+U\s+\.\s*S\s+\.\s+\d+(?:\s*,\s*\d+)?(?:\s*\(\s*\d{4}\s*\))?)"
)

DATE_RE = re.compile(
    r"((January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}\s*,?\s+\d{4})"
)

def read_blocks(path):
    text = path.read_text(encoding="utf-8").strip()
    return [b for b in text.split("\n\n") if b.strip()]

def block_to_tokens(block):
    rows = []
    for line in block.splitlines():
        if not line.strip():
            continue
        tok, gold = line.split("\t")
        rows.append((tok, gold))
    return rows

def apply_span_labels(tokens, pred, regex, label):
    text = " ".join(tokens)
    offsets = []
    cur = 0
    for tok in tokens:
        start = cur
        end = cur + len(tok)
        offsets.append((start, end))
        cur = end + 1

    for m in regex.finditer(text):
        s, e = m.span()
        idxs = [
            i for i, (ts, te) in enumerate(offsets)
            if ts >= s and te <= e
        ]
        if not idxs:
            continue
        pred[idxs[0]] = "B-" + label
        for i in idxs[1:]:
            pred[i] = "I-" + label

def main():
    blocks = read_blocks(INPUT_FILE)

    with OUTPUT_FILE.open("w", encoding="utf-8") as out:
        for block in blocks:
            rows = block_to_tokens(block)
            tokens = [r[0] for r in rows]
            golds = [r[1] for r in rows]
            pred = ["O"] * len(tokens)

            apply_span_labels(tokens, pred, CASE_CITATION_RE, "CITATION")
            apply_span_labels(tokens, pred, US_CITATION_RE, "CITATION")
            apply_span_labels(tokens, pred, DATE_RE, "DATE")

            for tok, gold, p in zip(tokens, golds, pred):
                out.write(f"{tok}\t{gold}\t{p}\n")
            out.write("\n")

    print(f"Done: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
