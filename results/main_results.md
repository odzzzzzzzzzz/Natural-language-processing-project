# Main Experimental Results

## Dataset Statistics

| Split | Sentences | Tokens | Entity Spans | CITATION | COURT | DATE | ORG | PARTY | STATUTE | JUDGE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Train | 106 | 135195 | 2652 | 786 | 282 | 189 | 98 | 833 | 315 | 149 |
| Dev | 13 | 21450 | 397 | 152 | 55 | 39 | 17 | 98 | 24 | 12 |
| Test | 14 | 7975 | 196 | 37 | 29 | 23 | 17 | 87 | 1 | 2 |
| Total | 133 | 164620 | 3245 | 975 | 366 | 251 | 132 | 1018 | 340 | 163 |

## Final Token-Level Results

| Model | Precision | Recall | F1 |
|---|---:|---:|---:|
| Majority | 0.000 | 0.000 | 0.000 |
| Stanza | 0.160 | 0.172 | 0.166 |
| Rule-Based | 0.799 | 0.334 | 0.471 |
| Original CRF | 0.803 | 0.601 | 0.688 |
| Tuned CRF | 0.843 | 0.651 | 0.734 |

## Final Span-Level Exact-Match Results

| Model | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| Majority | 0.000 | 0.000 | 0.000 | 0 | 0 | 68 |
| CoNLL-2003 CRF Transfer | 0.087 | 0.061 | 0.072 | 12 | 126 | 184 |
| Stanza | 0.157 | 0.240 | 0.190 | 47 | 252 | 149 |
| Rule-Based | 0.652 | 0.153 | 0.248 | 30 | 16 | 166 |
| Original CRF | 0.781 | 0.418 | 0.545 | 82 | 23 | 114 |
| Tuned CRF | 0.822 | 0.449 | 0.581 | 88 | 19 | 108 |

## Stage 4 Post-processing Results

| System | Precision | Recall | F1 | Main Finding |
|---|---:|---:|---:|---|
| Original CRF | 0.781 | 0.418 | 0.545 | Baseline before tuning |
| CRF + BIO Repair | 0.781 | 0.418 | 0.545 | No effect |
| CRF + Full Post-processing | 0.621 | 0.327 | 0.428 | Harmful due to over-expansion |
| Tuned CRF | 0.822 | 0.449 | 0.581 | Final best system |

## Per-Entity Token-Level F1 for Final Tuned CRF

| Entity Type | Token-Level F1 | TP | FP | FN |
|---|---:|---:|---:|---:|
| CITATION | 0.792 | 238 | 63 | 62 |
| COURT | 0.987 | 117 | 3 | 0 |
| DATE | 0.857 | 75 | 0 | 25 |
| JUDGE | 1.000 | 6 | 0 | 0 |
| ORG | 0.462 | 6 | 0 | 14 |
| PARTY | 0.274 | 31 | 22 | 142 |
| STATUTE | 0.000 | 0 | 0 | 11 |

## Per-Entity Span-Level F1 for Final Tuned CRF

| Entity Type | Span-Level F1 | TP | FP | FN |
|---|---:|---:|---:|---:|
| CITATION | 0.685 | 25 | 11 | 12 |
| COURT | 0.983 | 29 | 1 | 0 |
| DATE | 0.878 | 18 | 0 | 5 |
| JUDGE | 1.000 | 2 | 0 | 0 |
| ORG | 0.300 | 3 | 0 | 14 |
| PARTY | 0.210 | 11 | 7 | 76 |
| STATUTE | 0.000 | 0 | 0 | 1 |

## Key Takeaways

The tuned CRF is the final best-performing system. It achieves token-level F1 of 0.734 and strict span-level exact-match F1 of 0.581.

The CoNLL-2003 CRF transfer baseline performs poorly, with only 0.072 span-level F1. This confirms that general-domain CRF training does not transfer well to legal-specific NER.

The rule-based system has relatively high precision but very low recall. This confirms that hand-written legal patterns capture some reliable structures but miss many context-dependent entities.

The pretrained Stanza baseline performs poorly under the legal-specific schema, especially because it does not naturally model CITATION, COURT, STATUTE, or JUDGE.

Hyperparameter tuning improves both token-level and span-level CRF performance. The original CRF achieved token-level F1 of 0.688 and span-level F1 of 0.545, while the tuned CRF improves to token-level F1 of 0.734 and span-level F1 of 0.581.

The strongest tuned CRF categories are COURT, DATE, JUDGE, and CITATION. PARTY remains the weakest high-frequency entity type, and STATUTE remains unreliable because the test set contains only one statute span.

Stage 4 post-processing was fully tested, but full heuristic post-processing reduced performance because span completion over-expanded predicted citation boundaries. BIO repair, nested resolution, and type consistency alone had no effect.
