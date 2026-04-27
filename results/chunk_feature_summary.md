# Chunk Feature Experiment Summary

## Motivation

The original feature plan included chunk features as Group D. To test whether shallow syntactic information helps legal NER, we trained a chunk-augmented CRF using POS tags and a lightweight NLTK regex chunker.

The chunk-augmented CRF used the tuned regularization parameters:

| Parameter | Value |
|---|---:|
| c1 | 0.01 |
| c2 | 0.1 |

The model was trained on train + dev and evaluated on the held-out test set.

## Chunking Method

We used a simple regex chunk grammar over POS tags:

- NP chunks for noun phrases
- VP chunks for verb phrases
- PP chunks for prepositions

These chunk tags were added as CRF features, including current, previous, next, previous-2, and next-2 chunk tags.

## Overall Results

| Model | Token Precision | Token Recall | Token F1 | Span Precision | Span Recall | Span F1 |
|---|---:|---:|---:|---:|---:|---:|
| Tuned CRF | 0.843 | 0.651 | 0.734 | 0.822 | 0.449 | 0.581 |
| CRF + Chunk | 0.845 | 0.638 | 0.727 | 0.802 | 0.454 | 0.580 |

## Span-Level Per-Entity Results for CRF + Chunk

| Entity Type | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CITATION | 0.706 | 0.649 | 0.676 | 24 | 10 | 13 |
| COURT | 0.967 | 1.000 | 0.983 | 29 | 1 | 0 |
| DATE | 1.000 | 0.870 | 0.930 | 20 | 0 | 3 |
| JUDGE | 1.000 | 1.000 | 1.000 | 2 | 0 | 0 |
| ORG | 1.000 | 0.176 | 0.300 | 3 | 0 | 14 |
| PARTY | 0.550 | 0.126 | 0.206 | 11 | 9 | 76 |
| STATUTE | 0.000 | 0.000 | 0.000 | 0 | 2 | 1 |

## Token-Level Per-Entity Results for CRF + Chunk

| Entity Type | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CITATION | 0.809 | 0.720 | 0.762 | 216 | 51 | 84 |
| COURT | 0.975 | 1.000 | 0.987 | 117 | 3 | 0 |
| DATE | 1.000 | 0.870 | 0.930 | 87 | 0 | 13 |
| JUDGE | 1.000 | 1.000 | 1.000 | 6 | 0 | 0 |
| ORG | 1.000 | 0.300 | 0.462 | 6 | 0 | 14 |
| PARTY | 0.561 | 0.185 | 0.278 | 32 | 25 | 141 |
| STATUTE | 0.000 | 0.000 | 0.000 | 0 | 6 | 11 |

## Interpretation

Chunk features produced a model that was very close to the tuned CRF but did not surpass it. Span-level F1 was 0.580, compared with 0.581 for the tuned CRF. Token-level F1 was 0.727, compared with 0.734 for the tuned CRF.

This suggests that shallow syntactic chunk information is not harmful, but it does not provide a clear improvement over the tuned lexical and orthographic CRF. The chunk model improves DATE span-level F1 from 0.878 to 0.930 and gives strong CITATION performance, but it does not solve the hardest categories. PARTY remains weak, with span-level F1 of 0.206, and STATUTE remains 0.000.

The result suggests that the main remaining errors are not simply shallow phrase-boundary errors. They are legal-semantic errors involving party/citation ambiguity and rare statute examples.

## Paper-Ready Paragraph

We also tested chunk features, corresponding to the planned Group D feature set. We used POS tags and a lightweight regex chunker to generate NP, VP, and PP chunk tags, which were then added as CRF features. The chunk-augmented CRF achieved 0.580 span-level F1 and 0.727 token-level F1, nearly matching but not exceeding the tuned CRF, which achieved 0.581 span-level F1 and 0.734 token-level F1. Chunk features improved DATE recognition, raising DATE span-level F1 to 0.930, but they did not resolve the main weakness of the system: PARTY remained low at 0.206 span-level F1, and STATUTE remained 0.000. This suggests that shallow syntactic features are not sufficient for the central legal-semantic ambiguities in this task.

## Presentation Version

We also tested chunk features using a simple NP/VP/PP regex chunker. The result was almost tied with the tuned CRF: 0.580 span F1 versus 0.581. This means chunk features are not harmful, but they do not clearly improve the final model. They help DATE somewhat, but they still do not solve PARTY or STATUTE.
