# Gazetteer Feature Experiment Summary

## Motivation

The original feature plan included gazetteer/domain lexicon features as Group E. To test whether legal-domain lexicons improve performance, we trained a gazetteer-augmented CRF using the tuned regularization parameters:

| Parameter | Value |
|---|---:|
| c1 | 0.01 |
| c2 | 0.1 |

The gazetteer-augmented CRF was trained on train + dev and evaluated on the held-out test set.

## Gazetteer Feature Groups

The implemented gazetteer features include:

- court terms: court, supreme, appeals, district, circuit, justice, judge
- judge titles: justice, judge, chief, magistrate
- citation terms: U.S., F., Supp., S.Ct., L.Ed., No., v., supra, id.
- statute terms: U.S.C., section, title, act, code, statute, article, amendment
- party suffixes: Inc., Co., Corp., LLC, Department, Commission, Agency
- legal connectors: v., versus, ex rel., in re
- month names for DATE recognition

## Overall Results

| Model | Token Precision | Token Recall | Token F1 | Span Precision | Span Recall | Span F1 |
|---|---:|---:|---:|---:|---:|---:|
| Tuned CRF | 0.843 | 0.651 | 0.734 | 0.822 | 0.449 | 0.581 |
| CRF + Gazetteer | 0.877 | 0.616 | 0.724 | 0.811 | 0.439 | 0.570 |

## Span-Level Per-Entity Results for CRF + Gazetteer

| Entity Type | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CITATION | 0.688 | 0.595 | 0.638 | 22 | 10 | 15 |
| COURT | 0.967 | 1.000 | 0.983 | 29 | 1 | 0 |
| DATE | 1.000 | 0.870 | 0.930 | 20 | 0 | 3 |
| JUDGE | 1.000 | 1.000 | 1.000 | 2 | 0 | 0 |
| ORG | 1.000 | 0.176 | 0.300 | 3 | 0 | 14 |
| PARTY | 0.588 | 0.115 | 0.192 | 10 | 7 | 77 |
| STATUTE | 0.000 | 0.000 | 0.000 | 0 | 2 | 1 |

## Token-Level Per-Entity Results for CRF + Gazetteer

| Entity Type | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CITATION | 0.864 | 0.677 | 0.759 | 203 | 32 | 97 |
| COURT | 0.975 | 1.000 | 0.987 | 117 | 3 | 0 |
| DATE | 1.000 | 0.870 | 0.930 | 87 | 0 | 13 |
| JUDGE | 1.000 | 1.000 | 1.000 | 6 | 0 | 0 |
| ORG | 1.000 | 0.300 | 0.462 | 6 | 0 | 14 |
| PARTY | 0.569 | 0.168 | 0.259 | 29 | 22 | 144 |
| STATUTE | 0.000 | 0.000 | 0.000 | 0 | 6 | 11 |

## Interpretation

Gazetteer features did not improve the final model overall. Span-level F1 decreased from 0.581 to 0.570, and token-level F1 decreased from 0.734 to 0.724.

However, the gazetteer features helped DATE recognition. DATE span-level F1 increased from 0.878 in the tuned CRF to 0.930 in the gazetteer-augmented CRF. This makes sense because month names and date-like surface patterns can be captured by lexicon features.

The gazetteer features did not solve the main weakness of the system. PARTY span-level F1 stayed low at 0.192, and STATUTE remained 0.000. This suggests that simple legal lexicons are not enough to resolve the hardest legal NER distinctions, especially party names inside or near citations.

## Paper-Ready Paragraph

We also tested gazetteer features, corresponding to the planned Group E feature set. The gazetteer-augmented CRF included lexicons for court terms, judge titles, citation markers, statute terms, party suffixes, legal connectors, and month names. Overall, this feature group did not improve the final model: span-level F1 decreased from 0.581 to 0.570, and token-level F1 decreased from 0.734 to 0.724. The main benefit appeared in DATE recognition, where span-level F1 increased from 0.878 to 0.930. However, gazetteer features did not improve the hardest categories, especially PARTY and STATUTE. This suggests that while legal lexicons can help with surface-regular categories, they are insufficient for resolving legal-semantic ambiguity in party and citation contexts.

## Presentation Version

We tried adding legal gazetteer features, including court words, citation markers, statute words, party suffixes, and month names. This helped DATE recognition, but it did not improve the model overall. Span F1 dropped slightly from 0.581 to 0.570. The main takeaway is that lexicons help with surface patterns, but they do not solve the hard legal-semantic cases like PARTY and STATUTE.
