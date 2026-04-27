import random
from src.utils.data_loader import list_opinions, load_opinion_text, iter_paragraphs


RAW_DIR = "data/raw/1K_scotus"
OUTPUT_FILE = "data/annotated/sample_passages.txt"


def main():
    opinions = list_opinions(RAW_DIR)

    all_paragraphs = []

    for op_id in opinions:
        try:
            text = load_opinion_text(op_id, RAW_DIR)
            paras = list(iter_paragraphs(text))

            # 过滤太短的段落
            paras = [p for p in paras if len(p.split()) > 20]

            all_paragraphs.extend(paras)

        except Exception as e:
            print(f"skip {op_id}: {e}")

    print(f"Total paragraphs collected: {len(all_paragraphs)}")

    sample = random.sample(all_paragraphs, 150)

    with open(OUTPUT_FILE, "w") as f:
        for i, para in enumerate(sample):
            f.write(f"### SAMPLE {i}\n")
            f.write(para + "\n\n")

    print(f"Saved 150 samples to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
