# CRF Hyperparameter Tuning Summary

## Motivation

The original CRF model used fixed regularization parameters:

| Parameter | Value |
|---|---:|
| c1 | 0.1 |
| c2 | 0.1 |

To improve the model and make the experiment more systematic, we performed a development-set grid search over CRF regularization parameters.

## Search Space

| Parameter | Values |
|---|---|
| c1 | 0.01, 0.1, 0.5, 1.0 |
| c2 | 0.01, 0.1, 0.5, 1.0 |

The selection metric was development-set span-level exact-match F1.

## Best Development Configuration

| c1 | c2 | Dev Span Precision | Dev Span Recall | Dev Span F1 | Dev Token F1 |
|---:|---:|---:|---:|---:|---:|
| 0.01 | 0.1 | 0.671 | 0.519 | 0.585 | 0.516 |

The best configuration was then retrained on train + dev and evaluated on the held-out test set.

## Test Set Comparison

| Model | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| Original CRF | 0.781 | 0.418 | 0.545 | 82 | 23 | 114 |
| Tuned CRF | 0.822 | 0.449 | 0.581 | 88 | 19 | 108 |

## Per-Entity Test F1 Comparison

| Entity Type | Original CRF F1 | Tuned CRF F1 | Change |
|---|---:|---:|---:|
| CITATION | 0.571 | 0.685 | +0.114 |
| COURT | 0.983 | 0.983 | 0.000 |
| DATE | 0.905 | 0.878 | -0.027 |
| JUDGE | 0.667 | 1.000 | +0.333 |
| ORG | 0.300 | 0.300 | 0.000 |
| PARTY | 0.192 | 0.210 | +0.018 |
| STATUTE | 0.000 | 0.000 | 0.000 |

## Interpretation

Hyperparameter tuning improved the CRF's strict span-level F1 from 0.545 to 0.581. Both precision and recall improved: precision increased from 0.781 to 0.822, while recall increased from 0.418 to 0.449.

The largest meaningful improvement occurred for CITATION, whose span-level F1 increased from 0.571 to 0.685. PARTY also improved slightly, from 0.192 to 0.210, although it remains the weakest high-frequency entity type.

The tuned model should therefore be treated as the final CRF system in the paper and presentation.

## Paper-Ready Paragraph

We performed a development-set grid search over the CRF regularization parameters c1 and c2, using span-level exact-match F1 as the selection metric. The best configuration was c1=0.01 and c2=0.1, with development span-level F1 of 0.585. After retraining on train plus development data, the tuned CRF achieved 0.822 precision, 0.449 recall, and 0.581 span-level F1 on the held-out test set, improving over the original CRF's F1 of 0.545. The improvement was especially clear for CITATION, whose F1 increased from 0.571 to 0.685. This shows that systematic regularization tuning improves legal-domain CRF performance and that the tuned CRF should be used as the final reported model.
