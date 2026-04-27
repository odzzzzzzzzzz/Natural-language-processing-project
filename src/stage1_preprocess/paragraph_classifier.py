from pathlib import Path
import re
from collections import Counter

INPUT_JSON = Path("data/annotated/iaa_yulong.json")
OUTPUT_REPORT = Path("results/paragraph_classifier_report.txt")

INTRO_CONNECTIVES = {
    "however", "therefore", "thus", "accordingly", "nevertheless",
    "although", "because", "since", "first", "second", "finally",
    "in this case", "we hold", "we conclude", "the question is",
    "this case", "petitioner", "respondent"
}

CONCLUSION_CUES = {
    "affirmed", "reversed", "vacated", "remanded", "dismissed",
    "it is so ordered", "the judgment is", "for the foregoing reasons",
    "accordingly", "we affirm", "we reverse", "we remand"
}

def normalize(text):
    return re.sub(r"\s+", " ", text.strip().lower())

def tokenize(text):
    return re.findall(r"[A-Za-z]+|\d+|[^\w\s]", text)

def jaccard_similarity(a, b):
    ta = {t.lower() for t in tokenize(a) if t.isalpha()}
    tb = {t.lower() for t in tokenize(b) if t.isalpha()}
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)

def classify_paragraph(paragraph, index, total):
    p = normalize(paragraph)

    intro_score = 0
    conclusion_score = 0

    if index == 0:
        intro_score += 3
    if index == 1:
        intro_score += 1

    if index == total - 1:
        conclusion_score += 3
    if index == total - 2:
        conclusion_score += 1

    for cue in INTRO_CONNECTIVES:
        if cue in p:
            intro_score += 1

    for cue in CONCLUSION_CUES:
        if cue in p:
            conclusion_score += 2

    if re.search(r"\b(no\.|argued|decided|supreme court|certiorari)\b", p):
        intro_score += 1

    if conclusion_score > intro_score:
        return "CONCLUSION"
    if intro_score > conclusion_score:
        return "INTRODUCTION"
    return "BODY"

def split_paragraphs(text):
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if len(paras) <= 1:
        # Label Studio passages may already be 1 paragraph; fall back to sentence-like chunks
        paras = [p.strip() for p in re.split(r"(?<=[.!?])\s+(?=[A-Z])", text) if p.strip()]
    return paras

def main():
    import json

    data = json.loads(INPUT_JSON.read_text(encoding="utf-8"))

    label_counts = Counter()
    merge_candidates = 0
    examples = []

    for item in data:
        text = item["data"]["text"]
        paras = split_paragraphs(text)

        labels = []
        for i, para in enumerate(paras):
            lab = classify_paragraph(para, i, len(paras))
            labels.append(lab)
            label_counts[lab] += 1

        for i in range(len(paras) - 1):
            sim = jaccard_similarity(paras[i], paras[i + 1])
            if sim >= 0.25:
                merge_candidates += 1
                if len(examples) < 5:
                    examples.append((sim, paras[i][:180], paras[i + 1][:180]))

    lines = []
    lines.append("# Paragraph Classification Heuristic Report")
    lines.append("")
    lines.append("## Label counts")
    for k, v in label_counts.items():
        lines.append(f"- {k}: {v}")

    lines.append("")
    lines.append("## Adjacent paragraph merge candidates")
    lines.append(f"- Candidate pairs with Jaccard similarity >= 0.25: {merge_candidates}")

    lines.append("")
    lines.append("## Example merge candidates")
    for sim, p1, p2 in examples:
        lines.append(f"\nSimilarity={sim:.3f}")
        lines.append(f"Paragraph A: {p1}")
        lines.append(f"Paragraph B: {p2}")

    report = "\n".join(lines)
    print(report)
    OUTPUT_REPORT.write_text(report + "\n", encoding="utf-8")
    print(f"\nSaved report to {OUTPUT_REPORT}")

if __name__ == "__main__":
    main()
