import json
from pathlib import Path

INPUT_FILE = Path("data/annotated/sample_passages.txt")
OUTPUT_FILE = Path("data/annotated/sample_passages_labelstudio.jsonl")


def clean_leading_artifact(text: str) -> str:
    """
    Remove leading section/OCR artifacts such as:
    C
    B
    28
    1818
    """
    lines = text.splitlines()

    while lines:
        first = lines[0].strip()

        if not first:
            lines = lines[1:]
            continue

        # remove very short section headers like C, B, 28
        if len(first) <= 4 and (first.isalpha() or first.isdigit()):
            lines = lines[1:]
            continue

        break

    return "\n".join(lines).strip()


def main():
    content = INPUT_FILE.read_text(encoding="utf-8")
    chunks = content.split("### SAMPLE")

    records = []

    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue

        lines = chunk.splitlines()
        sample_id = lines[0].strip()
        text = "\n".join(lines[1:]).strip()
        text = clean_leading_artifact(text)

        if not text:
            continue

        records.append({
            "id": f"sample_{int(sample_id):03d}",
            "text": text,
        })

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Saved {len(records)} records to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
