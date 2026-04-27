# Token-Level Evaluation Results

## Final Token-Level Results

| Model | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| Majority | 0.000 | 0.000 | 0.000 | 0 | 0 | 667 |
| Stanza | 0.160 | 0.172 | 0.166 | 125 | 654 | 602 |
| Rule-Based | 0.799 | 0.334 | 0.471 | 243 | 61 | 484 |
| Original CRF | 0.803 | 0.601 | 0.688 | 437 | 107 | 290 |
| Tuned CRF | 0.843 | 0.651 | 0.734 | 473 | 88 | 254 |

## Per-Entity Token-Level F1

| Entity Type | Majority | Stanza | Rule-Based | Original CRF | Tuned CRF |
|---|---:|---:|---:|---:|---:|
| CITATION | 0.000 | 0.000 | 0.657 | 0.687 | 0.792 |
| COURT | 0.000 | 0.000 | 0.000 | 0.987 | 0.987 |
| DATE | 0.000 | 0.710 | 0.798 | 0.895 | 0.857 |
| ORG | 0.000 | 0.056 | 0.000 | 0.462 | 0.462 |
| PARTY | 0.000 | 0.149 | 0.000 | 0.266 | 0.274 |
| STATUTE | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| JUDGE | 0.000 | 0.000 | 0.000 | 0.800 | 1.000 |

## Key Takeaways

The tuned CRF is the best token-level system, achieving precision 0.843, recall 0.651, and F1 0.734.

Compared with the original CRF, tuning improves token-level F1 from 0.688 to 0.734. The largest improvement is on CITATION, whose token-level F1 increases from 0.687 to 0.792.

The tuned CRF remains weak on PARTY and STATUTE. PARTY improves slightly from 0.266 to 0.274, while STATUTE remains at 0.000 because the test set contains very few statute tokens and the model does not recover them.

The token-level score is higher than the span-level score because token-level evaluation gives partial credit for partially correct entity spans, while span-level exact-match evaluation requires exact boundaries and entity type.
