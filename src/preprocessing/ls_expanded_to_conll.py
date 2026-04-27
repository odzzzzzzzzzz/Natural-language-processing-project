import json
import re
from pathlib import Path

INPUT_JSON = Path("data/annotated/expanded_150_annotated.json")
OUTPUT_CONLL = Path("data/annotated/expanded_150.conll")

def tokenize_with_offsets(text):
    pattern = re.compile(r"\w+|[^\w\s]")
    return [(m.group(), m.start(), m.end()) for m in pattern.finditer(text)]

def main():
    data = json.load(open(INPUT_JSON, encoding="utf-8"))

    with OUTPUT_CONLL.open("w", encoding="utf-8") as out:
        used_tasks = 0

        for item in data:
            text = item.get("data", {}).get("text", "")
            if not text:
                continue

            tokens = tokenize_with_offsets(text)
            labels = ["O"] * len(tokens)

            anns = item.get("annotations", [])
            results = []
            for ann in anns:
                results.extend(ann.get("result", []))

            if not results:
                continue

            used_tasks += 1

            for r in results:
                if r.get("type") != "labels":
                    continue

                value = r.get("value", {})
                start = value.get("start")
                end = value.get("end")
                labs = value.get("labels", [])

                if start is None or end is None or not labs:
                    continue

                label = labs[0]

                matched = []
                for i, (_, tok_start, tok_end) in enumerate(tokens):
                    if tok_end <= start or tok_start >= end:
                        continue
                    matched.append(i)

                if not matched:
                    continue

                labels[matched[0]] = "B-" + label
                for i in matched[1:]:
                    labels[i] = "I-" + label

            for (tok, _, _), lab in zip(tokens, labels):
                out.write(f"{tok}\t{lab}\n")
            out.write("\n")

    print(f"Used annotated tasks: {used_tasks}")
    print(f"Saved CoNLL to {OUTPUT_CONLL}")

if __name__ == "__main__":
    main()
