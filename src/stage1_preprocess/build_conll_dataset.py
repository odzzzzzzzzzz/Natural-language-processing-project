import nltk
from src.utils.data_loader import load_opinion_text, iter_paragraphs

RAW_DIR = "data/raw/1K_scotus"
INPUT_FILE = "data/annotated/sample_passages.txt"
OUTPUT_FILE = "data/annotated/sample.conll"


def word_shape(word):
    shape = ""
    for c in word:
        if c.isupper():
            shape += "X"
        elif c.islower():
            shape += "x"
        elif c.isdigit():
            shape += "d"
        else:
            shape += c
    return shape


def process_paragraph(para):
    tokens = nltk.word_tokenize(para)
    pos_tags = nltk.pos_tag(tokens)

    lines = []
    for word, pos in pos_tags:
        shape = word_shape(word)
        lines.append(f"{word}\t{pos}\tO\t{shape}\tO\tO")
    return lines


def main():
    with open(INPUT_FILE, "r") as f:
        content = f.read()

    samples = content.split("### SAMPLE")

    all_lines = []

    for sample in samples:
        sample = sample.strip()
        if not sample:
            continue

        lines = sample.split("\n")
        paragraph = " ".join(lines[1:]).strip()

        if not paragraph:
            continue

        conll_lines = process_paragraph(paragraph)

        all_lines.extend(conll_lines)
        all_lines.append("")  # sentence separator

    with open(OUTPUT_FILE, "w") as f:
        for line in all_lines:
            f.write(line + "\n")

    print(f"Saved CoNLL dataset to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
