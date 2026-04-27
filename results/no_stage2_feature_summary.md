# No-Stage2 / No Rule-Output Feature Experiment Summary

## Motivation

Earlier CRF ablation suggested that the Stage 2 rule-output feature group might introduce noise. In the original development ablation, removing Group F improved development F1. However, the final tuned CRF still included the Stage 2 rule-output feature. Therefore, we trained a new CRF variant without any Stage 2 rule-output features to test whether removing these features improves final held-out test performance.

This experiment uses the tuned regularization parameters:

| Parameter | Value |
|---|---:|
| c1 | 0.01 |
| c2 | 0.1 |

The model was trained on train + dev and evaluated on the held-out test set.

## Overall Results

| Model | Token Precision | Token Recall | Token F1 | Span Precision | Span Recall | Span F1 |
|---|---:|---:|---:|---:|---:|---:|
| Tuned CRF | 0.843 | 0.651 | 0.734 | 0.822 | 0.449 | 0.581 |
| CRF NoStage2 | 0.820 | 0.646 | 0.723 | 0.819 | 0.439 | 0.571 |

## Span-Level Per-Entity Results for CRF NoStage2

| Entity Type | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CITATION | 0.697 | 0.622 | 0.657 | 23 | 10 | 14 |
| COURT | 0.967 | 1.000 | 0.983 | 29 | 1 | 0 |
| DATE | 1.000 | 0.870 | 0.930 | 20 | 0 | 3 |
| JUDGE | 1.000 | 1.000 | 1.000 | 2 | 0 | 0 |
| ORG | 1.000 | 0.176 | 0.300 | 3 | 0 | 14 |
| PARTY | 0.562 | 0.103 | 0.175 | 9 | 7 | 78 |
| STATUTE | 0.000 | 0.000 | 0.000 | 0 | 1 | 1 |

## Token-Level Per-Entity Results for CRF NoStage2

| Entity Type | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CITATION | 0.738 | 0.750 | 0.744 | 225 | 80 | 75 |
| COURT | 0.975 | 1.000 | 0.987 | 117 | 3 | 0 |
| DATE | 1.000 | 0.870 | 0.930 | 87 | 0 | 13 |
| JUDGE | 1.000 | 1.000 | 1.000 | 6 | 0 | 0 |
| ORG | 1.000 | 0.300 | 0.462 | 6 | 0 | 14 |
| PARTY | 0.630 | 0.168 | 0.265 | 29 | 17 | 144 |
| STATUTE | 0.000 | 0.000 | 0.000 | 0 | 3 | 11 |

## Interpretation

Removing Stage 2 rule-output features does not improve the final model. The NoStage2 CRF achieves 0.571 span-level F1, slightly below the tuned CRF's 0.581. Token-level F1 also decreases from 0.734 to 0.723.

This result complicates the earlier development-set ablation. On the development set, removing Group F appeared helpful, suggesting that rule-output features could introduce noise. However, on the held-out test set after tuning and retraining on train + dev, removing Stage 2 features slightly hurts performance. Therefore, the safest conclusion is that Stage 2 rule-output features are not a major source of improvement, but they are also not clearly harmful in the final tuned configuration.

The entity-level pattern shows that NoStage2 improves DATE span-level F1 to 0.930, but it lowers PARTY span-level F1 from 0.210 to 0.175 and lowers overall F1. Since PARTY is the hardest high-frequency entity type, the final tuned CRF remains preferable.

## Paper-Ready Paragraph

We also tested a NoStage2 CRF variant that removes the Stage 2 rule-output feature group. This experiment was motivated by the earlier development-set ablation, where removing rule-output features improved development F1. However, on the held-out test set after hyperparameter tuning, the NoStage2 model did not outperform the tuned CRF. Its span-level F1 was 0.571, compared with 0.581 for the tuned CRF, and its token-level F1 was 0.723, compared with 0.734. This suggests that the rule-output feature group is not a major driver of performance, but it is also not clearly harmful in the final tuned setting. We therefore keep the tuned CRF as the final best system.

## Presentation Version

We also tested removing the Stage 2 rule-output features. This almost matched the tuned CRF, but did not beat it: span F1 was 0.571 versus 0.581. So the rule features are not hugely important, but removing them does not improve the final model.
