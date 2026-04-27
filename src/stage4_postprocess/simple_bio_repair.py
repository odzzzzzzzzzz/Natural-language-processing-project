import argparse
from pathlib import Path

def norm(tag):
    return tag.strip().replace("−", "-").replace("–", "-").replace("—", "-")

def split_tag(tag):
    tag = norm(tag)
    if tag == "O" or tag == "":
        return "O", None
    if "-" not in tag:
        return "B", tag
    p, t = tag.split("-", 1)
    if p not in {"B", "I"}:
        p = "B"
    return p, t

def repair_tags(tags):
    repaired = []
    prev_prefix = "O"
    prev_type = None
    changes = 0

    for tag in tags:
        tag = norm(tag)
        prefix, typ = split_tag(tag)

        if prefix == "I":
            if prev_prefix == "O" or prev_type != typ:
                new_tag = f"B-{typ}"
                repaired.append(new_tag)
                changes += 1
                prev_prefix, prev_type = "B", typ
            else:
                repaired.append(tag)
                prev_prefix, prev_type = prefix, typ

        elif prefix == "B":
            repaired.append(tag)
            prev_prefix, prev_type = prefix, typ

        else:
            repaired.append("O")
            prev_prefix, prev_type = "O", None

    return repaired, changes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    sentences = []
    cur = []

    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                if cur:
                    sentences.append(cur)
                    cur = []
                continue

            parts = line.split("\t")
            cur.append(parts)

    if cur:
        sentences.append(cur)

    total_changes = 0
    output_lines = []

    for sent in sentences:
        pred_tags = [parts[-1] for parts in sent]
        repaired_tags, changes = repair_tags(pred_tags)
        total_changes += changes

        for parts, new_pred in zip(sent, repaired_tags):
            parts[-1] = new_pred
            output_lines.append("\t".join(parts))
        output_lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(output_lines), encoding="utf-8")

    print(f"Saved repaired file to {output_path}")
    print(f"Number of BIO repairs: {total_changes}")

if __name__ == "__main__":
    main()
