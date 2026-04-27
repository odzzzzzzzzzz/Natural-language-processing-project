# Full Stage 4 Post-processing Experiment

## Motivation

The original project plan included a Stage 4 post-processing module with three intended functions:

1. Span completion
2. Type consistency voting
3. Nested entity resolution

Earlier, we only tested a minimal BIO repair step. To complete the Stage 4 experiment more fully, we implemented a heuristic post-processing module that includes:

- BIO repair
- CITATION span completion
- PARTY span completion
- COURT span completion
- nested/overlap resolution
- document-level type consistency voting

## Post-processing Statistics

| Operation | Count |
|---|---:|
| BIO repairs | 0 |
| Span completions | 34 |
| Nested/overlap resolutions | 2 |
| Type consistency mappings | 5 |
| Type consistency changes | 0 |
| Total tag changes | 84 |

The type-consistency mappings learned from repeated predicted spans were:

| Span String | Consistent Type |
|---|---|
| february 4, 1879 | DATE |
| united states | PARTY |
| supreme court of united states | COURT |
| district court | COURT |
| court of appeals | COURT |

## Overall Results

| System | Precision | Recall | F1 |
|---|---:|---:|---:|
| CRF | 0.781 | 0.418 | 0.545 |
| CRF + BIO Repair | 0.781 | 0.418 | 0.545 |
| CRF + Full Post-processing | 0.621 | 0.327 | 0.428 |

## Per-Entity Span-Level F1

| Entity Type | CRF F1 | Full Post-processing F1 | Change |
|---|---:|---:|---:|
| CITATION | 0.571 | 0.147 | -0.424 |
| COURT | 0.983 | 0.949 | -0.034 |
| DATE | 0.905 | 0.905 | 0.000 |
| JUDGE | 0.667 | 0.667 | 0.000 |
| ORG | 0.300 | 0.300 | 0.000 |
| PARTY | 0.192 | 0.154 | -0.038 |
| STATUTE | 0.000 | 0.000 | 0.000 |

## Interpretation

Full heuristic post-processing reduced span-level F1 from 0.545 to 0.428. The largest degradation occurred for CITATION, whose F1 dropped from 0.571 to 0.147. This suggests that the citation span-completion heuristic was too aggressive under strict span-level exact-match evaluation.

The post-processing module made 84 token-level tag changes, including 34 span completions. However, these local changes often expanded predicted spans beyond the gold boundaries. Since span-level evaluation requires exact boundary matches, even a plausible but slightly overextended citation span is counted as incorrect.

This result is useful because it shows that legal NER post-processing cannot simply expand spans based on surface patterns. Citation spans are boundary-sensitive, and post-processing must be calibrated on development data before being applied to the test set.

## Paper-Ready Paragraph

We implemented a fuller Stage 4 post-processing module with BIO repair, span completion, nested-overlap resolution, and type consistency voting. However, this heuristic post-processing reduced strict span-level F1 from 0.545 to 0.428. The degradation was concentrated in CITATION, where F1 dropped from 0.571 to 0.147. Error inspection suggests that the citation span-completion heuristic often overextended predicted spans, which is heavily penalized by exact-match evaluation. This negative result indicates that legal NER post-processing must be designed conservatively and tuned on development data; naive span expansion can damage otherwise correct predictions.

## Presentation Version

We also tested a fuller Stage 4 cleanup module, including span completion and type consistency. Surprisingly, it hurt performance: span F1 dropped from 0.545 to 0.428. Most of the damage came from CITATION spans, where the cleanup rules often expanded predictions too far. This tells us that citation boundaries are very sensitive, and simple cleanup rules are not enough.
