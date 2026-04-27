import json
import re
from pathlib import Path

INPUT_FILE = Path("data/annotated/iaa_yulong.json")
OUTPUT_FILE = Path("data/annotated/iaa_yulong.conll")

def tokenize_with_offsets(text):
    tokens = []
    for m in re.finditer(r"\w+|[^\w\s]", text):
        tokens.append((m.group(), m.start(), m.end()))
    return tokens

def convert():
    with INPUT_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as out:
        for item in data:
            text = item["data"]["text"]
            tokens = tokenize_with_offsets(text)
            labels = ["O"] * len(tokens)

            for ann in item.get("annotations", []):
                for r in ann.get("result", []):
                    value = r.get("value", {})
                    start = value.get("start")
                    end = value.get("end")
                    label_list = value.get("labels", [])
                    if start is None or end is None or not label_list:
                        continue

                    label = label_list[0]
                    inside = [
                        i for i, (_, tok_start, tok_end) in enumerate(tokens)
                        if tok_start >= start and tok_end <= end
                    ]

                    if inside:
                        labels[inside[0]] = "B-" + label
                        for i in inside[1:]:
                            labels[i] = "I-" + label

            for (tok, _, _), lab in zip(tokens, labels):
                out.write(f"{tok}\t{lab}\n")
            out.write("\n")

    print(f"Done: {OUTPUT_FILE}")

if __name__ == "__main__":
    convert()
