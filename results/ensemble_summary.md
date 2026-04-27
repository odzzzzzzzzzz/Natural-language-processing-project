# Ensemble Experiment Summary

## Motivation

The original project plan included an optional enhanced system combining rule-based extraction and CRF predictions. The motivation was to test whether high-precision rule-based predictions could recover entities missed by the CRF, especially legal surface-pattern entities such as CITATION, DATE, and STATUTE.

We tested two ensemble variants:

1. Tuned CRF + Rule-Based system
2. NoStage2 CRF + Rule-Based system

The ensemble logic preserves the CRF prediction by default, but selectively adds or replaces high-precision rule-based spans for CITATION, DATE, and STATUTE.

## Ensemble Statistics

### Tuned CRF + Rule-Based

| Operation | Count |
|---|---:|
| Rule spans seen | 46 |
| Rule spans added | 4 |
| Rule spans replaced | 1 |
| Rule spans skipped | 41 |
| Overlap resolutions | 0 |

### NoStage2 CRF + Rule-Based

| Operation | Count |
|---|---:|
| Rule spans seen | 46 |
| Rule spans added | 5 |
| Rule spans replaced | 1 |
| Rule spans skipped | 40 |
| Overlap resolutions | 0 |

## Overall Results

| Model | Token Precision | Token Recall | Token F1 | Span Precision | Span Recall | Span F1 |
|---|---:|---:|---:|---:|---:|---:|
| Tuned CRF | 0.843 | 0.651 | 0.734 | 0.822 | 0.449 | 0.581 |
| Ensemble TunedRule | 0.819 | 0.662 | 0.732 | 0.793 | 0.449 | 0.573 |
| NoStage2 CRF | 0.820 | 0.646 | 0.723 | 0.819 | 0.439 | 0.571 |
| Ensemble NoStage2Rule | 0.800 | 0.664 | 0.726 | 0.782 | 0.439 | 0.562 |

## Span-Level Per-Entity Results: Ensemble TunedRule

| Entity Type | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CITATION | 0.650 | 0.703 | 0.675 | 26 | 14 | 11 |
| COURT | 0.967 | 1.000 | 0.983 | 29 | 1 | 0 |
| DATE | 0.944 | 0.739 | 0.829 | 17 | 1 | 6 |
| JUDGE | 1.000 | 1.000 | 1.000 | 2 | 0 | 0 |
| ORG | 1.000 | 0.176 | 0.300 | 3 | 0 | 14 |
| PARTY | 0.611 | 0.126 | 0.210 | 11 | 7 | 76 |
| STATUTE | 0.000 | 0.000 | 0.000 | 0 | 0 | 1 |

## Span-Level Per-Entity Results: Ensemble NoStage2Rule

| Entity Type | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CITATION | 0.632 | 0.649 | 0.640 | 24 | 14 | 13 |
| COURT | 0.967 | 1.000 | 0.983 | 29 | 1 | 0 |
| DATE | 0.950 | 0.826 | 0.884 | 19 | 1 | 4 |
| JUDGE | 1.000 | 1.000 | 1.000 | 2 | 0 | 0 |
| ORG | 1.000 | 0.176 | 0.300 | 3 | 0 | 14 |
| PARTY | 0.562 | 0.103 | 0.175 | 9 | 7 | 78 |
| STATUTE | 0.000 | 0.000 | 0.000 | 0 | 1 | 1 |

## Interpretation

The ensemble systems did not improve over the tuned CRF. The TunedRule ensemble slightly increased token-level recall and CITATION span recall, but it reduced precision enough that overall span-level F1 dropped from 0.581 to 0.573. The NoStage2Rule ensemble also failed to improve span-level F1, dropping from 0.571 to 0.562.

This suggests that the rule-based system is useful as a standalone high-precision baseline, but naive rule-CRF ensembling does not reliably improve strict span-level exact-match performance. The main problem is boundary sensitivity: even when rules recover plausible legal spans, they can introduce small boundary or type mismatches that are penalized under exact-match span evaluation.

## Paper-Ready Paragraph

We also tested two rule-CRF ensemble systems as an enhanced model experiment. The first combined the tuned CRF with the rule-based system, while the second combined the NoStage2 CRF with the rule-based system. The ensemble selectively added or replaced high-precision rule spans for CITATION, DATE, and STATUTE. However, neither ensemble improved over the tuned CRF. The TunedRule ensemble achieved 0.573 span-level F1, below the tuned CRF's 0.581, while the NoStage2Rule ensemble achieved 0.562 span-level F1. Although the ensemble increased CITATION recall, it also reduced precision, showing that naive rule-CRF voting can introduce boundary noise under strict exact-match evaluation.

## Presentation Version

We also tried an enhanced ensemble system combining CRF predictions with rule-based predictions. It did not beat the tuned CRF. The ensemble recovered a few extra citation spans, but it also added boundary noise, so span F1 dropped from 0.581 to 0.573. This shows that rules are useful as a baseline, but naive voting is not enough.
