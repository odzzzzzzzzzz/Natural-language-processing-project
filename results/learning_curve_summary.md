# Learning Curve / Annotation Size Experiment

## Motivation

This experiment tests whether additional annotated legal data improves CRF performance.

We trained the same tuned CRF architecture on different fractions of the train + dev pool and evaluated every model on the same held-out test set.

The fixed CRF parameters were:

| c1 | c2 |
|---:|---:|
| 0.01 | 0.1 |

Each training fraction was repeated with three random seeds.

## Summary Results

| Training Fraction | Train Units | Mean Precision | Mean Recall | Mean Span F1 | Individual F1 Scores |
|---:|---:|---:|---:|---:|---|
| 0.25 | 30 | 0.795 | 0.374 | 0.508 | 0.488, 0.532, 0.504 |
| 0.50 | 60 | 0.796 | 0.384 | 0.518 | 0.542, 0.519, 0.493 |
| 0.75 | 89 | 0.840 | 0.427 | 0.566 | 0.564, 0.569, 0.566 |
| 1.00 | 119 | 0.820 | 0.449 | 0.580 | 0.581, 0.581, 0.579 |

## Individual Runs

| Fraction | Seed | Train Units | Precision | Recall | Span F1 | TP | FP | FN |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.25 | 13 | 30 | 0.727 | 0.367 | 0.488 | 72 | 27 | 124 |
| 0.25 | 21 | 30 | 0.804 | 0.398 | 0.532 | 78 | 19 | 118 |
| 0.25 | 42 | 30 | 0.854 | 0.357 | 0.504 | 70 | 12 | 126 |
| 0.50 | 13 | 60 | 0.808 | 0.408 | 0.542 | 80 | 19 | 116 |
| 0.50 | 21 | 60 | 0.784 | 0.388 | 0.519 | 76 | 21 | 120 |
| 0.50 | 42 | 60 | 0.795 | 0.357 | 0.493 | 70 | 18 | 126 |
| 0.75 | 13 | 89 | 0.863 | 0.418 | 0.564 | 82 | 13 | 114 |
| 0.75 | 21 | 89 | 0.825 | 0.434 | 0.569 | 85 | 18 | 111 |
| 0.75 | 42 | 89 | 0.832 | 0.429 | 0.566 | 84 | 17 | 112 |
| 1.00 | 13 | 119 | 0.822 | 0.449 | 0.581 | 88 | 19 | 108 |
| 1.00 | 21 | 119 | 0.822 | 0.449 | 0.581 | 88 | 19 | 108 |
| 1.00 | 42 | 119 | 0.815 | 0.449 | 0.579 | 88 | 20 | 108 |

## Interpretation

The learning curve shows a clear positive relationship between annotation size and span-level performance.

Mean span-level F1 increases from 0.508 with 25% of the train + dev data to 0.580 with 100% of the train + dev data. The strongest jump occurs between the 50% and 75% conditions, where mean F1 rises from 0.518 to 0.566.

This supports the claim that additional in-domain legal annotation improves legal NER performance. However, the improvement from 75% to 100% is smaller, suggesting that data size is not the only bottleneck. The remaining errors are also related to boundary ambiguity, PARTY/CITATION overlap, rare labels such as STATUTE, and the limitations of a flat BIO tagging schema.

## Paper-Ready Paragraph

To measure the effect of annotation size, we ran a learning-curve experiment using the tuned CRF architecture. We trained models on 25%, 50%, 75%, and 100% of the train plus development pool, repeating each condition with three random seeds and evaluating all models on the same held-out test set. Mean strict span-level F1 increased from 0.508 at 25% of the data to 0.518 at 50%, 0.566 at 75%, and 0.580 at 100%. This confirms that additional in-domain legal annotation improves CRF performance. At the same time, the relatively small improvement from 75% to 100% suggests that the remaining errors are not only caused by limited data, but also by legal-specific boundary ambiguity, especially in PARTY and CITATION contexts.

## Presentation Version

We also ran a learning-curve experiment. As we increased the amount of annotated training data, span-level F1 improved from about 0.508 with 25% of the data to 0.580 with the full train + dev set. This shows that more legal annotation helps. However, the gain becomes smaller near the full-data setting, meaning that the remaining errors are not just a data-size problem; they also reflect difficult PARTY/CITATION boundary ambiguity.
