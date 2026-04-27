from pathlib import Path
import argparse
import json
from collections import Counter, defaultdict
import joblib
import sklearn_crfsuite
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans

ROOT = Path(__file__).resolve().parents[2]

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
    return tok.lower()

def build_context_documents(sentences, max_vocab=5000, min_count=2):
    counts = Counter()

    for sent in sentences:
        for item in sent:
            counts[norm(item["token"])] += 1

    vocab = [
        word for word, count in counts.most_common(max_vocab)
        if count >= min_count
    ]

    context_docs = defaultdict(list)

    vocab_set = set(vocab)

    for sent in sentences:
        tokens = [norm(x["token"]) for x in sent]

        for i, word in enumerate(tokens):
            if word not in vocab_set:
                continue

            prev1 = tokens[i - 1] if i > 0 else "BOS"
            next1 = tokens[i + 1] if i + 1 < len(tokens) else "EOS"
            prev2 = tokens[i - 2] if i >= 2 else "BOS2"
            next2 = tokens[i + 2] if i + 2 < len(tokens) else "EOS2"

            raw = sent[i]["token"]

            context_docs[word].extend([
                f"prev1={prev1}",
                f"next1={next1}",
                f"prev2={prev2}",
                f"next2={next2}",
                f"shape={shape(raw)}",
                f"prefix2={word[:2]}",
                f"prefix3={word[:3]}",
                f"suffix2={word[-2:]}",
                f"suffix3={word[-3:]}",
                f"has_digit={any(c.isdigit() for c in raw)}",
                f"has_period={'.' in raw}",
                f"is_cap={raw[:1].isupper()}",
            ])

    words = sorted(context_docs.keys())
    docs = [" ".join(context_docs[w]) for w in words]

    return words, docs

def build_word_clusters(sentences, n_clusters=50, max_vocab=5000, min_count=2):
    words, docs = build_context_documents(
        sentences,
        max_vocab=max_vocab,
        min_count=min_count,
    )

    if not words:
        return {}

    actual_clusters = min(n_clusters, len(words))

    print(f"Word-cluster vocabulary size: {len(words)}")
    print(f"Number of clusters: {actual_clusters}")

    vectorizer = TfidfVectorizer(
        min_df=1,
        max_features=20000,
        token_pattern=r"(?u)\b\S+\b",
    )
    X = vectorizer.fit_transform(docs)

    kmeans = MiniBatchKMeans(
        n_clusters=actual_clusters,
        random_state=13,
        batch_size=512,
        n_init=10,
    )
    labels = kmeans.fit_predict(X)

    mapping = {
        word: f"CL{int(label):03d}"
        for word, label in zip(words, labels)
    }

    return mapping

def cluster_for_token(tok, cluster_map):
    low = norm(tok)

    if low in cluster_map:
        return cluster_map[low]

    if any(c.isdigit() for c in tok):
        return "UNK_HAS_DIGIT"
    if tok[:1].isupper():
        return "UNK_CAPITALIZED"
    if "." in tok:
        return "UNK_HAS_PERIOD"

    return "UNK"

def token_features(sent, i, cluster_map):
    tok = sent[i]["token"]
    lower = tok.lower()
    cluster = cluster_for_token(tok, cluster_map)

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

        # Group H: distributional word-cluster features
        "H:cluster": cluster,
        "H:cluster_prefix2": cluster[:4],
        "H:is_unknown_cluster": cluster.startswith("UNK"),

        # Group F: rule/stage2 output if available
        "F:stage2_tag": sent[i].get("stage2", "O"),
    }

    if i == 0:
        feats["G:BOS"] = True
    else:
        prev = sent[i - 1]["token"]
        feats["A:prev_word"] = prev.lower()
        feats["B:prev_shape"] = shape(prev)
        feats["H:prev_cluster"] = cluster_for_token(prev, cluster_map)
        feats["F:prev_stage2_tag"] = sent[i - 1].get("stage2", "O")

    if i == len(sent) - 1:
        feats["G:EOS"] = True
    else:
        nxt = sent[i + 1]["token"]
        feats["A:next_word"] = nxt.lower()
        feats["B:next_shape"] = shape(nxt)
        feats["H:next_cluster"] = cluster_for_token(nxt, cluster_map)
        feats["F:next_stage2_tag"] = sent[i + 1].get("stage2", "O")

    if i >= 2:
        prev2 = sent[i - 2]["token"]
        feats["A:prev2_word"] = prev2.lower()
        feats["H:prev2_cluster"] = cluster_for_token(prev2, cluster_map)

    if i + 2 < len(sent):
        next2 = sent[i + 2]["token"]
        feats["A:next2_word"] = next2.lower()
        feats["H:next2_cluster"] = cluster_for_token(next2, cluster_map)

    return feats

def sent2features(sent, cluster_map):
    return [token_features(sent, i, cluster_map) for i in range(len(sent))]

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
    parser.add_argument("--output", default="data/splits/test_crf_wordcluster_pred.conll")
    parser.add_argument("--model_out", default="models/crf_wordcluster.pkl")
    parser.add_argument("--cluster_out", default="models/word_clusters.json")
    parser.add_argument("--c1", type=float, default=0.01)
    parser.add_argument("--c2", type=float, default=0.1)
    parser.add_argument("--max_iterations", type=int, default=100)
    parser.add_argument("--n_clusters", type=int, default=50)
    parser.add_argument("--max_vocab", type=int, default=5000)
    parser.add_argument("--min_count", type=int, default=2)
    args = parser.parse_args()

    train_sents = read_conll(ROOT / args.train)
    dev_sents = read_conll(ROOT / args.dev)
    test_sents = read_conll(ROOT / args.test)

    train_dev_sents = train_sents + dev_sents

    print(f"Train sentences: {len(train_sents)}")
    print(f"Dev sentences: {len(dev_sents)}")
    print(f"Train+Dev sentences: {len(train_dev_sents)}")
    print(f"Test sentences: {len(test_sents)}")

    print("Building distributional word clusters from train+dev...")
    cluster_map = build_word_clusters(
        train_dev_sents,
        n_clusters=args.n_clusters,
        max_vocab=args.max_vocab,
        min_count=args.min_count,
    )

    cluster_out = ROOT / args.cluster_out
    cluster_out.parent.mkdir(parents=True, exist_ok=True)
    cluster_out.write_text(
        json.dumps(cluster_map, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(f"Saved word clusters to {cluster_out}")

    X_train = [sent2features(s, cluster_map) for s in train_dev_sents]
    y_train = [sent2labels(s) for s in train_dev_sents]
    X_test = [sent2features(s, cluster_map) for s in test_sents]

    print(f"Training word-cluster CRF with c1={args.c1}, c2={args.c2}...")
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
