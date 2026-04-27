# POS Feature Experiment Summary

## Motivation

The original feature plan included POS features as Group C. Earlier CRF experiments used lexical/contextual, orthographic, rule-output, and boundary features, but did not include POS tags. To test whether POS information helps legal NER, we trained a POS-augmented CRF using the tuned regularization parameters:

| Parameter | Value |
|---|---:|
| c1 | 0.01 |
| c2 | 0.1 |

The POS-augmented CRF was trained on train + dev and evaluated on the held-out test set.

## Overall Results

| Model | Token Precision | Token Recall | Token F1 | Span Precision | Span Recall | Span F1 |
|---|---:|---:|---:|---:|---:|---:|
| Tuned CRF | 0.843 | 0.651 | 0.734 | 0.822 | 0.449 | 0.581 |
| CRF + POS | 0.828 | 0.597 | 0.694 | 0.787 | 0.434 | 0.559 |

## Span-Level Per-Entity Results for CRF + POS

| Entity Type | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CITATION | 0.647 | 0.595 | 0.620 | 22 | 12 | 15 |
| COURT | 0.967 | 1.000 | 0.983 | 29 | 1 | 0 |
| DATE | 1.000 | 0.783 | 0.878 | 18 | 0 | 5 |
| JUDGE | 1.000 | 1.000 | 1.000 | 2 | 0 | 0 |
| ORG | 1.000 | 0.176 | 0.300 | 3 | 0 | 14 |
| PARTY | 0.550 | 0.126 | 0.206 | 11 | 9 | 76 |
| STATUTE | 0.000 | 0.000 | 0.000 | 0 | 1 | 1 |

## Token-Level Per-Entity Results for CRF + POS

| Entity Type | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CITATION | 0.773 | 0.660 | 0.712 | 198 | 58 | 102 |
| COURT | 0.975 | 1.000 | 0.987 | 117 | 3 | 0 |
| DATE | 1.000 | 0.750 | 0.857 | 75 | 0 | 25 |
| JUDGE | 1.000 | 1.000 | 1.000 | 6 | 0 | 0 |
| ORG | 1.000 | 0.300 | 0.462 | 6 | 0 | 14 |
| PARTY | 0.552 | 0.185 | 0.277 | 32 | 26 | 141 |
| STATUTE | 0.000 | 0.000 | 0.000 | 0 | 3 | 11 |

## Interpretation

Adding POS features did not improve the final CRF. Span-level F1 decreased from 0.581 to 0.559, and token-level F1 decreased from 0.734 to 0.694.

This suggests that general-purpose POS tags are not very informative for the legal-specific entity distinctions in this task. Legal NER requires recognizing domain-specific spans such as case citations, statutes, courts, and parties. These distinctions are not directly encoded by POS categories such as noun, proper noun, verb, or punctuation.

The POS-augmented model still performs well on COURT, DATE, and JUDGE, but it does not improve the hardest categories. PARTY remains weak, with span-level F1 of 0.206, and STATUTE remains 0.000. CITATION also drops compared with the tuned CRF, from 0.685 to 0.620 span-level F1.

## Paper-Ready Paragraph

We also tested POS features, corresponding to the planned Group C feature set. Using the tuned CRF regularization parameters, we trained a POS-augmented CRF on train plus development data and evaluated it on the held-out test set. POS features did not improve performance: span-level F1 decreased from 0.581 to 0.559, and token-level F1 decreased from 0.734 to 0.694. This suggests that general-purpose POS tags do not capture the legal-specific distinctions needed for entities such as CITATION, PARTY, COURT, and STATUTE. In particular, POS features did not resolve the main remaining weakness of the model, since PARTY and STATUTE remained difficult.

## Presentation Version

We also tried adding POS features, which were part of the original feature plan. This did not help: span F1 dropped from 0.581 to 0.559. The likely reason is that POS tags describe grammatical categories, but our hardest labels are legal-semantic categories. For example, knowing that a token is a proper noun does not tell us whether it is a PARTY, ORG, JUDGE, or part of a CITATION.
