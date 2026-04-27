from pathlib import Path
import stanza

INPUT_FILE = Path("data/splits/test.conll")
OUTPUT_FILE = Path("data/splits/test_stanza_pred.conll")

MAP = {
    "PERSON": "PARTY",
    "ORG": "ORG",
    "DATE": "DATE",
    "LAW": "STATUTE",
}

def read_conll(path):
    rows = []
    tokens = []
    golds = []

    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            if tokens:
                rows.append((tokens, golds))
                tokens, golds = [], []
            continue
        parts = line.split("\t")
        tokens.append(parts[0])
        golds.append(parts[1])

    if tokens:
        rows.append((tokens, golds))

    return rows

def bio_from_entities(tokens, ents):
    labels = ["O"] * len(tokens)
    text = " ".join(tokens)

    offsets = []
    pos = 0
    for tok in tokens:
        start = pos
        end = pos + len(tok)
        offsets.append((start, end))
        pos = end + 1

    for ent in ents:
        mapped = MAP.get(ent.type)
        if not mapped:
            continue

        matched = []
        for i, (s, e) in enumerate(offsets):
            if e <= ent.start_char or s >= ent.end_char:
                continue
            matched.append(i)

        if matched:
            labels[matched[0]] = "B-" + mapped
            for i in matched[1:]:
                labels[i] = "I-" + mapped

    return labels

def main():
    print("Loading Stanza...")
    nlp = stanza.Pipeline("en", processors="tokenize,ner", tokenize_pretokenized=True)

    rows = read_conll(INPUT_FILE)

    with OUTPUT_FILE.open("w", encoding="utf-8") as out:
        for tokens, golds in rows:
            doc = nlp([tokens])
            ents = doc.ents
            preds = bio_from_entities(tokens, ents)

            for tok, gold, pred in zip(tokens, golds, preds):
                out.write(f"{tok}\t{gold}\t{pred}\n")
            out.write("\n")

    print(f"Saved Stanza predictions to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
