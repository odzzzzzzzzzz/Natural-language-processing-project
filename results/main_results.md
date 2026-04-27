# Main Experimental Results

## Dataset Statistics

| Split | Sentences | Tokens | Entity Spans | CITATION | COURT | DATE | ORG | PARTY | STATUTE | JUDGE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Train | 106 | 135195 | 2652 | 786 | 282 | 189 | 98 | 833 | 315 | 149 |
| Dev | 13 | 21450 | 397 | 152 | 55 | 39 | 17 | 98 | 24 | 12 |
| Test | 14 | 7975 | 196 | 37 | 29 | 23 | 17 | 87 | 1 | 2 |
| Total | 133 | 164620 | 3245 | 975 | 366 | 251 | 132 | 1018 | 340 | 163 |

## Token-Level Evaluation Results

| Model | Precision | Recall | F1 |
|---|---:|---:|---:|
| Majority | 0.000 | 0.000 | 0.000 |
| Stanza | 0.160 | 0.172 | 0.166 |
| Rule-Based | 0.799 | 0.334 | 0.471 |
| CRF | 0.803 | 0.601 | 0.688 |

## Span-Level Exact-Match Results

| Model | Precision | Recall | F1 |
|---|---:|---:|---:|
| Majority | 0.000 | 0.000 | 0.000 |
| Stanza | 0.157 | 0.240 | 0.190 |
| Rule-Based | 0.652 | 0.153 | 0.248 |
| CRF | 0.781 | 0.418 | 0.545 |

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

## Per-Entity Span-Level F1

| Entity Type | Rule-Based | Stanza | CRF |
|---|---:|---:|---:|
| CITATION | 0.424 | 0.000 | 0.571 |
| COURT | 0.000 | 0.000 | 0.983 |
| DATE | 0.800 | 0.415 | 0.905 |
| ORG | 0.000 | 0.144 | 0.300 |
| PARTY | 0.000 | 0.239 | 0.192 |
| STATUTE | 0.000 | 0.000 | 0.000 |
| JUDGE | 0.000 | 0.000 | 0.667 |

## Key Takeaways

The CRF model achieves the best performance under both token-level and span-level evaluation. Its token-level F1 is 0.688, while its stricter span-level exact-match F1 is 0.545.

The gap between token-level and span-level F1 shows that many remaining errors are boundary-sensitive. The model often identifies entity tokens correctly but does not always recover the exact full span.

The rule-based system has high token-level precision and reasonable citation/date performance, but its recall is low because it cannot capture non-formulaic or context-dependent legal entities.

The pretrained Stanza baseline performs poorly under the legal-specific schema, especially on CITATION, COURT, STATUTE, and JUDGE, confirming the domain mismatch problem.

The CRF performs very well on COURT and DATE, moderately on CITATION, and poorly on PARTY, ORG, and STATUTE. PARTY is the largest error source, while STATUTE and JUDGE are unstable because the test set contains very few examples.
