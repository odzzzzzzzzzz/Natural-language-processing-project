# Token-Level Evaluation Results

| Model | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| Majority | 0.000 | 0.000 | 0.000 | 0 | 0 | 667 |
| Stanza | 0.160 | 0.172 | 0.166 | 125 | 654 | 602 |
| Rule-Based | 0.799 | 0.334 | 0.471 | 243 | 61 | 484 |
| CRF | 0.803 | 0.601 | 0.688 | 437 | 107 | 290 |

## Per-Entity Token-Level F1

| Entity Type | Majority | Stanza | Rule-Based | CRF |
|---|---:|---:|---:|---:|
| CITATION | 0.000 | 0.000 | 0.657 | 0.687 |
| COURT | 0.000 | 0.000 | 0.000 | 0.987 |
| DATE | 0.000 | 0.710 | 0.798 | 0.895 |
| ORG | 0.000 | 0.056 | 0.000 | 0.462 |
| PARTY | 0.000 | 0.149 | 0.000 | 0.266 |
| STATUTE | 0.000 | 0.000 | 0.000 | 0.000 |
| JUDGE | 0.000 | 0.000 | 0.000 | 0.800 |