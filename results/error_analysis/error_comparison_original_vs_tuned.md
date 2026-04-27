# Error Comparison: Original CRF vs Tuned CRF

## Motivation

After hyperparameter tuning, the CRF's span-level exact-match F1 improved from 0.545 to 0.581. This file compares the error patterns of the original CRF and the tuned CRF to understand what changed.

## Overall Error Category Comparison

| Error Category | Original CRF | Tuned CRF | Change |
|---|---:|---:|---:|
| False negative | 99 | 96 | -3 |
| Boundary error | 10 | 6 | -4 |
| Type error | 7 | 6 | -1 |
| False positive | 6 | 7 | +1 |

## Main Interpretation

Hyperparameter tuning improves the model not only in aggregate F1 but also in the structure of its errors. The tuned CRF reduces false negatives, boundary errors, and type errors. The only category that slightly increases is false positives, from 6 to 7.

This means the tuned model becomes somewhat less conservative: it recovers more correct spans and reduces boundary mismatches, while introducing only one additional false positive.

## Entity-Specific Error Pattern for Tuned CRF

| Error Category | Entity Type | Count |
|---|---|---:|
| False negative | PARTY | 69 |
| False negative | ORG | 14 |
| False negative | CITATION | 8 |
| False negative | DATE | 5 |
| False positive | CITATION | 5 |
| Boundary error | PARTY | 4 |
| Type error | PARTY | 3 |
| Type error | CITATION | 2 |
| Boundary error | CITATION | 2 |
| Type error | STATUTE | 1 |
| False positive | COURT | 1 |
| False positive | PARTY | 1 |

## Key Finding 1: CITATION Improved

The tuned CRF improves CITATION substantially.

| Metric | Original CRF | Tuned CRF | Change |
|---|---:|---:|---:|
| CITATION span F1 | 0.571 | 0.685 | +0.114 |
| CITATION false negatives | 12 | 8 | -4 |
| CITATION boundary errors | 5 | 2 | -3 |

This suggests that hyperparameter tuning helped the CRF recover citation spans more accurately and reduced citation boundary mismatches.

## Key Finding 2: PARTY Remains the Main Weakness

PARTY remains the largest source of errors even after tuning.

| Metric | Original CRF | Tuned CRF | Change |
|---|---:|---:|---:|
| PARTY span F1 | 0.192 | 0.210 | +0.018 |
| PARTY false negatives | 68 | 69 | +1 |
| PARTY boundary errors | 5 | 4 | -1 |

Although PARTY F1 improves slightly, the number of missed PARTY entities remains extremely high. This confirms that PARTY recognition is not mainly a hyperparameter problem. It is a structural and linguistic problem caused by the way party names appear inside or near legal citations.

## Paper-Ready Paragraph

Hyperparameter tuning improved the CRF's span-level F1 from 0.545 to 0.581 and also changed the model's error profile. Compared with the original CRF, the tuned CRF reduces false negatives from 99 to 96, boundary errors from 10 to 6, and type errors from 7 to 6, while false positives increase only slightly from 6 to 7. The improvement is especially clear for CITATION: citation false negatives drop from 12 to 8, boundary errors drop from 5 to 2, and span-level F1 increases from 0.571 to 0.685. However, PARTY remains the dominant source of errors. The tuned model still misses 69 PARTY spans, showing that party recognition is not solved by regularization tuning alone. Instead, PARTY errors reflect a deeper legal-linguistic problem: party names often appear inside or near citation-like expressions, making their boundaries difficult to learn under a flat BIO schema.

## Presentation Version

Tuning improved the CRF, but it did not solve every problem. It helped most with CITATION: citation F1 increased from 0.571 to 0.685 and boundary errors dropped. But PARTY is still the main failure case. Even after tuning, the model misses 69 PARTY spans. So our final conclusion is that tuning improves citation boundary control, while PARTY recognition requires better annotation guidelines, more data, or a nested-entity strategy.
