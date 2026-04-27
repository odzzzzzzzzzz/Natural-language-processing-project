import argparse
from collections import Counter, defaultdict
from pathlib import Path

def split_tag(tag):
    tag = tag.strip().replace("−", "-").replace("–", "-").replace("—", "-")
    if tag == "O" or tag == "":
        return "O", None
    if "-" not in tag:
        return "B", tag
    prefix, typ = tag.split("-", 1)
    if prefix not in {"B", "I"}:
        prefix = "B"
    return prefix, typ

def read_conll(path):
    sentences = []
    cur = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                if cur:
                    sentences.append(cur)
                    cur = []
                continue

            parts = line.split("\t")
            if len(parts) < 3:
                continue

            token = parts[0]
            gold = parts[-2]
            pred = parts[-1]
            cur.append((token, pred, gold))

    if cur:
        sentences.append(cur)

    return sentences

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
    p = tp / (tp + fp) if tp + fp > 0 else 0.0
    r = tp / (tp + fn) if tp + fn > 0 else 0.0
    f1 = 2 * p * r / (p + r) if p + r > 0 else 0.0
    return p, r, f1

def evaluate(path, model):
    sentences = read_conll(path)

    pred_spans = []
    gold_spans = []

    for sid, sent in enumerate(sentences):
        pred_tags = [x[1] for x in sent]
        gold_tags = [x[2] for x in sent]
        pred_spans.extend(bio_to_spans(pred_tags, sid))
        gold_spans.extend(bio_to_spans(gold_tags, sid))

    pred_set = set(pred_spans)
    gold_set = set(gold_spans)

    correct = pred_set & gold_set

    tp = len(correct)
    fp = len(pred_set - gold_set)
    fn = len(gold_set - pred_set)

    p, r, f1 = prf(tp, fp, fn)

    types = sorted(set([s[3] for s in pred_spans] + [s[3] for s in gold_spans]))
    rows = []

    for typ in types:
        pred_t = {s for s in pred_set if s[3] == typ}
        gold_t = {s for s in gold_set if s[3] == typ}
        correct_t = pred_t & gold_t

        ttp = len(correct_t)
        tfp = len(pred_t - gold_t)
        tfn = len(gold_t - pred_t)

        pp, rr, ff = prf(ttp, tfp, tfn)
        rows.append((typ, pp, rr, ff, ttp, tfp, tfn))

    report = []
    report.append(f"# Span-Level Evaluation: {model}")
    report.append("")
    report.append("## Overall")
    report.append("")
    report.append("| Model | Precision | Recall | F1 | TP | FP | FN |")
    report.append("|---|---:|---:|---:|---:|---:|---:|")
    report.append(f"| {model} | {p:.3f} | {r:.3f} | {f1:.3f} | {tp} | {fp} | {fn} |")
    report.append("")
    report.append("## Per-Entity Type")
    report.append("")
    report.append("| Entity Type | Precision | Recall | F1 | TP | FP | FN |")
    report.append("|---|---:|---:|---:|---:|---:|---:|")
    for typ, pp, rr, ff, ttp, tfp, tfn in rows:
        report.append(f"| {typ} | {pp:.3f} | {rr:.3f} | {ff:.3f} | {ttp} | {tfp} | {tfn} |")

    text = "\n".join(report)
    out = Path("results") / f"span_eval_{model}.md"
    out.write_text(text, encoding="utf-8")

    print(text)
    print()
    print(f"Saved to {out}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--model", required=True)
    args = parser.parse_args()
    evaluate(args.input, args.model)

if __name__ == "__main__":
    main()
