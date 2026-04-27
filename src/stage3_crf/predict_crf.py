from pathlib import Path
import re
import joblib

MODEL_FILE = Path("models/crf_v1.pkl")
INPUT_FILE = Path("data/splits/test.conll")
OUTPUT_FILE = Path("data/splits/test_crf_pred.conll")

def shape(word):
    s = re.sub(r"[A-Z]", "X", word)
    s = re.sub(r"[a-z]", "x", s)
    s = re.sub(r"[0-9]", "d", s)
    return s

def read_conll(path):
    sents, sent = [], []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            if sent:
                sents.append(sent)
                sent = []
            continue
        parts = line.split("\t")
        tok, gold = parts[:2]
        stage2 = parts[2] if len(parts) >= 3 else "O"
        sent.append({"token": tok, "gold": gold, "stage2": stage2})
    if sent:
        sents.append(sent)
    return sents

def token_features(sent, i):
    tok = sent[i]["token"]
    lower = tok.lower()
    feats = {
        "bias": 1.0,
        "A:word.lower": lower,
        "A:suffix2": lower[-2:],
        "A:suffix3": lower[-3:],
        "A:suffix4": lower[-4:],
        "A:prefix2": lower[:2],
        "A:prefix3": lower[:3],
        "B:is_capitalized": tok[:1].isupper(),
        "B:is_all_upper": tok.isupper(),
        "B:is_title_case": tok.istitle(),
        "B:has_digit": any(c.isdigit() for c in tok),
        "B:has_period": "." in tok,
        "B:has_section_symbol": "§" in tok,
        "B:shape": shape(tok),
        "F:stage2_tag": sent[i].get("stage2", "O"),
    }

    if i == 0:
        feats["G:BOS"] = True
    else:
        prev = sent[i-1]["token"]
        feats["A:prev_word"] = prev.lower()
        feats["B:prev_shape"] = shape(prev)
        feats["F:prev_stage2_tag"] = sent[i-1].get("stage2", "O")

    if i == len(sent) - 1:
        feats["G:EOS"] = True
    else:
        nxt = sent[i+1]["token"]
        feats["A:next_word"] = nxt.lower()
        feats["B:next_shape"] = shape(nxt)
        feats["F:next_stage2_tag"] = sent[i+1].get("stage2", "O")

    if i >= 2:
        feats["A:prev2_word"] = sent[i-2]["token"].lower()
    if i + 2 < len(sent):
        feats["A:next2_word"] = sent[i+2]["token"].lower()

    return feats

def sent_features(sent):
    return [token_features(sent, i) for i in range(len(sent))]

def main():
    crf = joblib.load(MODEL_FILE)
    sents = read_conll(INPUT_FILE)
    X = [sent_features(s) for s in sents]
    y_pred = crf.predict(X)

    with OUTPUT_FILE.open("w", encoding="utf-8") as out:
        for sent, pred_sent in zip(sents, y_pred):
            for tok, pred in zip(sent, pred_sent):
                out.write(f"{tok['token']}\t{tok['gold']}\t{pred}\n")
            out.write("\n")

    print(f"Saved predictions to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
