from pathlib import Path
import argparse
import joblib
import sklearn_crfsuite

ROOT = Path(__file__).resolve().parents[2]

COURT_TERMS = {
    "court", "courts", "supreme", "appeals", "appeal", "district",
    "circuit", "tribunal", "judge", "judges", "justice", "justices"
}

JUDGE_TITLES = {
    "justice", "justices", "judge", "judges", "chief", "magistrate"
}

CITATION_TERMS = {
    "u", "s", "u.s", "u.s.", "f", "f.", "supp", "s.ct", "s.ct.",
    "l.ed", "l.ed.", "no", "nos", "v", "v.", "supra", "id", "ante"
}

STATUTE_TERMS = {
    "u.s.c", "u.s.c.", "usc", "section", "sections", "title",
    "act", "code", "statute", "statutes", "article", "amendment"
}

PARTY_SUFFIXES = {
    "inc", "inc.", "co", "co.", "corp", "corp.", "corporation",
    "company", "ltd", "ltd.", "llc", "association", "board",
    "department", "commission", "agency"
}

LEGAL_CONNECTORS = {
    "v", "v.", "versus", "ex", "rel", "in", "re"
}

MONTHS = {
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december"
}


def read_conll(path):
    sentences = []
    cur = []

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")

            if not line.strip():
                if cur:
                    sentences.append(cur)
                    cur = []
                continue

            parts = line.split("\t")

            if len(parts) == 2:
                token, gold = parts
                stage2 = "O"
            elif len(parts) >= 3:
                token, gold, stage2 = parts[0], parts[-2], parts[-1]
            else:
                continue

            cur.append({
                "token": token,
                "gold": gold,
                "stage2": stage2,
            })

    if cur:
        sentences.append(cur)

    return sentences


def shape(word):
    out = []
    for ch in word:
        if ch.isupper():
            out.append("X")
        elif ch.islower():
            out.append("x")
        elif ch.isdigit():
            out.append("d")
        else:
            out.append(ch)
    return "".join(out)


def norm(tok):
    return tok.lower().strip()


def strip_period(tok):
    return norm(tok).rstrip(".")


def is_reporter_pattern(tok):
    low = norm(tok)
    return (
        low in CITATION_TERMS
        or low.replace(".", "") in {"us", "usc", "fsupp", "sct", "led"}
    )


def token_features(sent, i):
    tok = sent[i]["token"]
    lower = tok.lower()
    clean = strip_period(tok)

    prev = sent[i - 1]["token"] if i > 0 else ""
    nxt = sent[i + 1]["token"] if i + 1 < len(sent) else ""

    prev_clean = strip_period(prev)
    next_clean = strip_period(nxt)

    feats = {
        "bias": 1.0,

        # Group A: lexical/contextual
        "A:word.lower": lower,
        "A:suffix2": lower[-2:],
        "A:suffix3": lower[-3:],
        "A:suffix4": lower[-4:],
        "A:prefix2": lower[:2],
        "A:prefix3": lower[:3],

        # Group B: orthographic
        "B:is_capitalized": tok[:1].isupper(),
        "B:is_all_upper": tok.isupper(),
        "B:is_title_case": tok.istitle(),
        "B:has_digit": any(c.isdigit() for c in tok),
        "B:has_period": "." in tok,
        "B:has_section_symbol": "§" in tok,
        "B:shape": shape(tok),

        # Group E: gazetteer/domain lexicon features
        "E:is_court_term": clean in COURT_TERMS,
        "E:is_judge_title": clean in JUDGE_TITLES,
        "E:is_citation_term": clean in CITATION_TERMS or is_reporter_pattern(tok),
        "E:is_statute_term": clean in STATUTE_TERMS or tok == "§",
        "E:is_party_suffix": clean in PARTY_SUFFIXES,
        "E:is_legal_connector": clean in LEGAL_CONNECTORS,
        "E:is_month": clean in MONTHS,

        "E:prev_is_court_term": prev_clean in COURT_TERMS,
        "E:next_is_court_term": next_clean in COURT_TERMS,
        "E:prev_is_citation_term": prev_clean in CITATION_TERMS or is_reporter_pattern(prev),
        "E:next_is_citation_term": next_clean in CITATION_TERMS or is_reporter_pattern(nxt),
        "E:prev_is_party_suffix": prev_clean in PARTY_SUFFIXES,
        "E:next_is_party_suffix": next_clean in PARTY_SUFFIXES,

        # Useful legal phrase indicators
        "E:prev_current_bigram": f"{prev_clean}_{clean}" if prev else "BOS",
        "E:current_next_bigram": f"{clean}_{next_clean}" if nxt else "EOS",
        "E:near_v_connector": prev_clean in LEGAL_CONNECTORS or next_clean in LEGAL_CONNECTORS,

        # Group F: rule/stage2 output if available
        "F:stage2_tag": sent[i].get("stage2", "O"),
    }

    if i == 0:
        feats["G:BOS"] = True
    else:
        feats["A:prev_word"] = prev.lower()
        feats["B:prev_shape"] = shape(prev)
        feats["F:prev_stage2_tag"] = sent[i - 1].get("stage2", "O")

    if i == len(sent) - 1:
        feats["G:EOS"] = True
    else:
        feats["A:next_word"] = nxt.lower()
        feats["B:next_shape"] = shape(nxt)
        feats["F:next_stage2_tag"] = sent[i + 1].get("stage2", "O")

    if i >= 2:
        prev2 = sent[i - 2]["token"]
        feats["A:prev2_word"] = prev2.lower()
        feats["E:prev2_is_citation_term"] = strip_period(prev2) in CITATION_TERMS or is_reporter_pattern(prev2)

    if i + 2 < len(sent):
        next2 = sent[i + 2]["token"]
        feats["A:next2_word"] = next2.lower()
        feats["E:next2_is_citation_term"] = strip_period(next2) in CITATION_TERMS or is_reporter_pattern(next2)

    return feats


def sent2features(sent):
    return [token_features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [x["gold"] for x in sent]


def write_predictions(sentences, predictions, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for sent, pred_sent in zip(sentences, predictions):
            for item, pred in zip(sent, pred_sent):
                f.write(f"{item['token']}\t{item['gold']}\t{pred}\n")
            f.write("\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", default="data/splits/train.conll")
    parser.add_argument("--dev", default="data/splits/dev.conll")
    parser.add_argument("--test", default="data/splits/test.conll")
    parser.add_argument("--output", default="data/splits/test_crf_gazetteer_pred.conll")
    parser.add_argument("--model_out", default="models/crf_gazetteer.pkl")
    parser.add_argument("--c1", type=float, default=0.01)
    parser.add_argument("--c2", type=float, default=0.1)
    parser.add_argument("--max_iterations", type=int, default=100)
    args = parser.parse_args()

    train_sents = read_conll(ROOT / args.train)
    dev_sents = read_conll(ROOT / args.dev)
    test_sents = read_conll(ROOT / args.test)

    train_dev_sents = train_sents + dev_sents

    print(f"Train sentences: {len(train_sents)}")
    print(f"Dev sentences: {len(dev_sents)}")
    print(f"Train+Dev sentences: {len(train_dev_sents)}")
    print(f"Test sentences: {len(test_sents)}")

    X_train = [sent2features(s) for s in train_dev_sents]
    y_train = [sent2labels(s) for s in train_dev_sents]
    X_test = [sent2features(s) for s in test_sents]

    print(f"Training gazetteer-augmented CRF with c1={args.c1}, c2={args.c2}...")
    crf = sklearn_crfsuite.CRF(
        algorithm="lbfgs",
        c1=args.c1,
        c2=args.c2,
        max_iterations=args.max_iterations,
        all_possible_transitions=True,
    )
    crf.fit(X_train, y_train)

    model_out = ROOT / args.model_out
    model_out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(crf, model_out)
    print(f"Saved model to {model_out}")

    print("Predicting test set...")
    preds = crf.predict(X_test)

    output = ROOT / args.output
    write_predictions(test_sents, preds, output)
    print(f"Saved predictions to {output}")


if __name__ == "__main__":
    main()
