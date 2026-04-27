# Word-Cluster Feature Experiment Summary

## Motivation

The original optional enhanced system included Brown cluster or word-cluster style features. To test this idea without relying on an external Brown clustering resource, we implemented a Brown-style distributional word-cluster feature experiment.

The model builds word clusters from the train + dev corpus. Each word is represented by local contextual features, including neighboring words, word shape, prefixes, suffixes, capitalization, digit patterns, and punctuation patterns. These context vectors are clustered with MiniBatchKMeans, and the resulting cluster id is added as a CRF feature.

This experiment uses the tuned CRF regularization parameters:

| Parameter | Value |
|---|---:|
| c1 | 0.01 |
| c2 | 0.1 |

The word-cluster CRF was trained on train + dev and evaluated on the held-out test set.

## Cluster Setup

| Setting | Value |
|---|---:|
| Vocabulary size | 5000 |
| Number of clusters | 50 |
| Minimum count | 2 |
| Clustering method | MiniBatchKMeans |
| Feature source | Train + dev context distribution |

## Overall Results

| Model | Token Precision | Token Recall | Token F1 | Span Precision | Span Recall | Span F1 |
|---|---:|---:|---:|---:|---:|---:|
| Tuned CRF | 0.843 | 0.651 | 0.734 | 0.822 | 0.449 | 0.581 |
| CRF + WordCluster | 0.821 | 0.613 | 0.702 | 0.780 | 0.434 | 0.557 |

## Span-Level Per-Entity Results for CRF + WordCluster

| Entity Type | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CITATION | 0.657 | 0.622 | 0.639 | 23 | 12 | 14 |
| COURT | 0.967 | 1.000 | 0.983 | 29 | 1 | 0 |
| DATE | 0.947 | 0.783 | 0.857 | 18 | 1 | 5 |
| JUDGE | 1.000 | 1.000 | 1.000 | 2 | 0 | 0 |
| ORG | 1.000 | 0.176 | 0.300 | 3 | 0 | 14 |
| PARTY | 0.526 | 0.115 | 0.189 | 10 | 9 | 77 |
| STATUTE | 0.000 | 0.000 | 0.000 | 0 | 1 | 1 |

## Token-Level Per-Entity Results for CRF + WordCluster

| Entity Type | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CITATION | 0.784 | 0.703 | 0.742 | 211 | 58 | 89 |
| COURT | 0.975 | 1.000 | 0.987 | 117 | 3 | 0 |
| DATE | 0.949 | 0.750 | 0.838 | 75 | 4 | 25 |
| JUDGE | 1.000 | 1.000 | 1.000 | 6 | 0 | 0 |
| ORG | 1.000 | 0.300 | 0.462 | 6 | 0 | 14 |
| PARTY | 0.517 | 0.179 | 0.266 | 31 | 29 | 142 |
| STATUTE | 0.000 | 0.000 | 0.000 | 0 | 3 | 11 |

## Interpretation

Word-cluster features did not improve the final model. Span-level F1 decreased from 0.581 to 0.557, and token-level F1 decreased from 0.734 to 0.702.

This suggests that distributional word clusters learned from the current pilot corpus are not strong enough to improve legal NER. The corpus is relatively small, so the learned clusters may be noisy. More importantly, the hardest labels in this task require legal-semantic distinctions, such as deciding whether a name is a PARTY, ORG, JUDGE, or part of a CITATION. These distinctions are not reliably captured by surface-level distributional clusters.

The word-cluster model still performs well on COURT and JUDGE, but it does not improve CITATION, PARTY, or STATUTE. PARTY remains weak, with span-level F1 of 0.189, and STATUTE remains 0.000.

## Paper-Ready Paragraph

We also tested Brown-style distributional word-cluster features as an optional enhanced feature experiment. We built word clusters from the train plus development corpus using local context features and MiniBatchKMeans, then added the resulting cluster ids to the CRF feature set. This did not improve performance: span-level F1 decreased from 0.581 to 0.557, and token-level F1 decreased from 0.734 to 0.702. This suggests that word clusters learned from the current pilot corpus are too noisy or too surface-level to resolve the legal-semantic distinctions required by this task. In particular, PARTY and STATUTE remained difficult, showing that the main remaining errors cannot be solved by distributional word-cluster features alone.

## Presentation Version

We also tried Brown-style word-cluster features. This did not help: span F1 dropped from 0.581 to 0.557. The likely reason is that our corpus is too small for stable clusters, and the hardest labels require legal-semantic judgment rather than just distributional similarity.
