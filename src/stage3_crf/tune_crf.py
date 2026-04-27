from pathlib import Path
import argparse
import csv
import joblib
import sklearn_crfsuite

ROOT = Path(__file__).resolve().parents[2]

def split_tag(tag):
    tag = tag.strip().replace("−", "-").replace("–", "-").replace("—", "-")
    if tag == "" or tag == "O":
        return "O", None
    if "-" not in tag:
        return "B", tag
    prefix, typ = tag.split("-", 1)
    if prefix not in {"B", "I"}:
        prefix = "B"
    return prefix, typ

def bio_to_spans(tags, sent_id):
    spans = []
    start = None
    cur_type = None

    for i, tag in enumerate(tags):
        prefix, typ = split_tag(tag)

        if prefix == "O":
            if cur_type is not None:
                spans.append((sent_id, start, i, cur_type))
                start = None
                cur_type = None
            continue

        if prefix == "B":
            if cur_type is not None:
                spans.append((sent_id, start, i, cur_type))
            start = i
            cur_type = typ
            continue

        if prefix == "I":
            if cur_type is None:
                start = i
                cur_type = typ
            elif typ != cur_type:
                spans.append((sent_id, start, i, cur_type))
                start = i
                cur_type = typ

    if cur_type is not None:
        spans.append((sent_id, start, len(tags), cur_type))

    return spans

def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f1

def span_f1(y_true, y_pred):
    gold = []
    pred = []

    for sid, (g_sent, p_sent) in enumerate(zip(y_true, y_pred)):
        gold.extend(bio_to_spans(g_sent, sid))
        pred.extend(bio_to_spans(p_sent, sid))

    gold_set = set(gold)
    pred_set = set(pred)

    tp = len(gold_set & pred_set)
    fp = len(pred_set - gold_set)
    fn = len(gold_set - pred_set)

    return (*prf(tp, fp, fn), tp, fp, fn)

def token_f1(y_true, y_pred):
    tp = fp = fn = 0

    for g_sent, p_sent in zip(y_true, y_pred):
        for gold, pred in zip(g_sent, p_sent):
            if pred != "O" and pred == gold:
                tp += 1
            elif pred != "O" and pred != gold:
                fp += 1
                if gold != "O":
                    fn += 1
            elif pred == "O" and gold != "O":
                fn += 1

    return (*prf(tp, fp, fn), tp, fp, fn)

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

def token_features(sent, i):
    tok = sent[i]["token"]
    lower = tok.lower()

    feats = {
        "bias": 1.0,

        # Group A: lexical and local context
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

        # Group F: rule / stage2 output if present
        "F:stage2_tag": sent[i].get("stage2", "O"),
    }

    if i == 0:
        feats["G:BOS"] = True
    else:
        prev = sent[i - 1]["token"]
        feats["A:prev_word"] = prev.lower()
        feats["B:prev_shape"] = shape(prev)
        feats["F:prev_stage2_tag"] = sent[i - 1].get("stage2", "O")

    if i == len(sent) - 1:
        feats["G:EOS"] = True
    else:
        nxt = sent[i + 1]["token"]
        feats["A:next_word"] = nxt.lower()
        feats["B:next_shape"] = shape(nxt)
        feats["F:next_stage2_tag"] = sent[i + 1].get("stage2", "O")

    if i >= 2:
        feats["A:prev2_word"] = sent[i - 2]["token"].lower()
    if i + 2 < len(sent):
        feats["A:next2_word"] = sent[i + 2]["token"].lower()

    return feats

def sent2features(sent):
    return [token_features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [x["gold"] for x in sent]

def write_predictions(sentences, predictions, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        for sent, pred_sent in zip(sentences, predictions):
            for item, pred in zip(sent, pred_sent):
                f.write(f"{item['token']}\t{item['gold']}\t{pred}\n")
            f.write("\n")

def train_crf(X_train, y_train, c1, c2, max_iterations):
    crf = sklearn_crfsuite.CRF(
        algorithm="lbfgs",
        c1=c1,
        c2=c2,
        max_iterations=max_iterations,
        all_possible_transitions=True,
    )
    crf.fit(X_train, y_train)
    return crf

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", default="data/splits/train.conll")
    parser.add_argument("--dev", default="data/splits/dev.conll")
    parser.add_argument("--test", default="data/splits/test.conll")
    parser.add_argument("--out_csv", default="results/crf_tuning.csv")
    parser.add_argument("--out_md", default="results/crf_tuning.md")
    parser.add_argument("--model_out", default="models/crf_tuned.pkl")
    parser.add_argument("--test_pred", default="data/splits/test_crf_tuned_pred.conll")
    parser.add_argument("--max_iterations", type=int, default=100)
    args = parser.parse_args()

    train_sents = read_conll(ROOT / args.train)
    dev_sents = read_conll(ROOT / args.dev)
    test_sents = read_conll(ROOT / args.test)

    X_train = [sent2features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]

    X_dev = [sent2features(s) for s in dev_sents]
    y_dev = [sent2labels(s) for s in dev_sents]

    X_test = [sent2features(s) for s in test_sents]

    c1_values = [0.01, 0.1, 0.5, 1.0]
    c2_values = [0.01, 0.1, 0.5, 1.0]

    rows = []
    best = None

    print(f"Train sentences: {len(train_sents)}")
    print(f"Dev sentences: {len(dev_sents)}")
    print(f"Test sentences: {len(test_sents)}")
    print("Starting CRF grid search...")

    for c1 in c1_values:
        for c2 in c2_values:
            print(f"\nTraining c1={c1}, c2={c2}")
            crf = train_crf(X_train, y_train, c1, c2, args.max_iterations)
            y_dev_pred = crf.predict(X_dev)

            span_p, span_r, span, span_tp, span_fp, span_fn = span_f1(y_dev, y_dev_pred)
            tok_p, tok_r, tok, tok_tp, tok_fp, tok_fn = token_f1(y_dev, y_dev_pred)

            row = {
                "c1": c1,
                "c2": c2,
                "dev_span_precision": span_p,
                "dev_span_recall": span_r,
                "dev_span_f1": span,
                "dev_span_tp": span_tp,
                "dev_span_fp": span_fp,
                "dev_span_fn": span_fn,
                "dev_token_precision": tok_p,
                "dev_token_recall": tok_r,
                "dev_token_f1": tok,
                "dev_token_tp": tok_tp,
                "dev_token_fp": tok_fp,
                "dev_token_fn": tok_fn,
            }
            rows.append(row)

            print(
                f"Dev span F1={span:.3f}, P={span_p:.3f}, R={span_r:.3f}; "
                f"token F1={tok:.3f}"
            )

            if best is None or row["dev_span_f1"] > best["dev_span_f1"]:
                best = row

    rows = sorted(rows, key=lambda x: x["dev_span_f1"], reverse=True)

    out_csv = ROOT / args.out_csv
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    out_md = ROOT / args.out_md
    lines = []
    lines.append("# CRF Hyperparameter Tuning")
    lines.append("")
    lines.append("This experiment performs dev-set grid search over CRF regularization parameters `c1` and `c2`.")
    lines.append("")
    lines.append("## Search Space")
    lines.append("")
    lines.append("- c1: 0.01, 0.1, 0.5, 1.0")
    lines.append("- c2: 0.01, 0.1, 0.5, 1.0")
    lines.append("- Selection metric: development span-level exact-match F1")
    lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append("| Rank | c1 | c2 | Dev Span P | Dev Span R | Dev Span F1 | Dev Token F1 |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|")

    for rank, row in enumerate(rows, 1):
        lines.append(
            f"| {rank} | {row['c1']} | {row['c2']} | "
            f"{row['dev_span_precision']:.3f} | {row['dev_span_recall']:.3f} | "
            f"{row['dev_span_f1']:.3f} | {row['dev_token_f1']:.3f} |"
        )

    lines.append("")
    lines.append("## Best Configuration")
    lines.append("")
    lines.append(f"- Best c1: {best['c1']}")
    lines.append(f"- Best c2: {best['c2']}")
    lines.append(f"- Best dev span F1: {best['dev_span_f1']:.3f}")
    lines.append(f"- Best dev token F1: {best['dev_token_f1']:.3f}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("This tuning experiment replaces the earlier fixed-parameter CRF setup with a systematic dev-set grid search. The selected configuration is then retrained on train+dev and evaluated on the held-out test set.")
    out_md.write_text("\n".join(lines), encoding="utf-8")

    print("\nBest configuration:")
    print(best)
    print(f"Saved tuning CSV to {out_csv}")
    print(f"Saved tuning summary to {out_md}")

    # Retrain on train + dev with best params.
    print("\nRetraining tuned CRF on train + dev...")
    train_dev_sents = train_sents + dev_sents
    X_train_dev = [sent2features(s) for s in train_dev_sents]
    y_train_dev = [sent2labels(s) for s in train_dev_sents]

    tuned = train_crf(
        X_train_dev,
        y_train_dev,
        best["c1"],
        best["c2"],
        args.max_iterations,
    )

    model_out = ROOT / args.model_out
    model_out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(tuned, model_out)
    print(f"Saved tuned model to {model_out}")

    print("Predicting test set with tuned CRF...")
    y_test_pred = tuned.predict(X_test)

    test_pred = ROOT / args.test_pred
    write_predictions(test_sents, y_test_pred, test_pred)
    print(f"Saved tuned CRF test predictions to {test_pred}")

if __name__ == "__main__":
    main()
