# Experiment Completion Summary

## Completed Experiments

| Component | Status | Output File | Notes |
|---|---|---|---|
| Dataset statistics | Completed | results/dataset_stats.md | Train/dev/test statistics and per-entity counts computed |
| Majority baseline | Completed | data/splits/test_majority_pred.conll | Predicts O for every token |
| Rule-based baseline | Completed | data/splits/test_rule_pred.conll | High precision but low recall |
| Stanza baseline | Completed | data/splits/test_stanza_pred.conll | General-domain pretrained baseline |
| CRF model | Completed | data/splits/test_crf_pred.conll | Main statistical sequence labeling model |
| Token-level evaluation | Completed | results/token_eval_results.md | CRF token-level F1 = 0.688 |
| Span-level exact-match evaluation | Completed | results/main_results.md | CRF span-level F1 = 0.545 |
| Per-entity evaluation | Completed | results/per_entity_span_comparison.md | CRF strong on COURT and DATE, weak on PARTY and STATUTE |
| Error analysis | Completed | results/error_analysis/crf_errors.md | Main error type is false negatives |
| Paper-ready error summary | Completed | results/error_analysis/error_summary_for_paper.md | Can be directly used in Discussion section |
| BIO repair post-processing | Completed | results/postprocess_summary.md | Did not improve CRF F1 |
| CRF feature ablation | Completed | results/ablation.md | Lexical/contextual features are most important |
| Ablation interpretation | Completed | results/ablation_summary_for_paper.md | Paper-ready explanation generated |
| Annotation provenance note | Completed | results/annotation_provenance_note.md | Explains 50-passage pilot and 150-passage main corpus |

## Main Results

### Token-Level Results

| Model | Precision | Recall | F1 |
|---|---:|---:|---:|
| Majority | 0.000 | 0.000 | 0.000 |
| Stanza | 0.160 | 0.172 | 0.166 |
| Rule-Based | 0.799 | 0.334 | 0.471 |
| CRF | 0.803 | 0.601 | 0.688 |

### Span-Level Exact-Match Results

| Model | Precision | Recall | F1 |
|---|---:|---:|---:|
| Majority | 0.000 | 0.000 | 0.000 |
| Stanza | 0.157 | 0.240 | 0.190 |
| Rule-Based | 0.652 | 0.153 | 0.248 |
| CRF | 0.781 | 0.418 | 0.545 |

## CRF Per-Entity Span-Level F1

| Entity Type | F1 | Interpretation |
|---|---:|---|
| COURT | 0.983 | Strong performance; stable patterns |
| DATE | 0.905 | Strong performance; regular surface forms |
| JUDGE | 0.667 | Reasonable but unstable because test set has only 2 examples |
| CITATION | 0.571 | Moderate; boundary errors remain common |
| ORG | 0.300 | Weak recall |
| PARTY | 0.192 | Main weakness; many false negatives |
| STATUTE | 0.000 | Unstable because test set has only 1 example |

## Error Analysis Summary

| Error Category | Count |
|---|---:|
| False negative | 99 |
| Boundary error | 10 |
| Type error | 7 |
| False positive | 6 |

Main finding: the CRF is conservative. It does not mainly hallucinate entities; instead, it misses many gold spans, especially PARTY entities.

## Ablation Summary

| Setting | Disabled Group | Dev Micro-F1 | F1 Drop |
|---|---:|---:|---:|
| All features |  | 0.509 | 0.000 |
| Without group A | A | 0.380 | 0.129 |
| Without group B | B | 0.470 | 0.039 |
| Without group F | F | 0.549 | -0.040 |
| Without group G | G | 0.508 | 0.001 |

Main finding: lexical and local contextual features are the most important. Removing Stage 2 rule-based features improves dev F1, suggesting that the current rule-based feature integration may add noise.

## Post-Processing Summary

| System | Precision | Recall | F1 |
|---|---:|---:|---:|
| CRF | 0.781 | 0.418 | 0.545 |
| CRF + BIO Repair | 0.781 | 0.418 | 0.545 |

Main finding: BIO repair does not change performance, so most errors are not caused by invalid BIO transitions.

## Incomplete or Limited Components

| Component | Status | How to Discuss |
|---|---|---|
| Inter-annotator agreement | Not completed | Report annotation provenance, not IAA |
| Full 800-1000 passage corpus | Not completed | Frame current work as pilot-scale |
| CoNLL-2003 transfer baseline | Not completed | Mention as future work if not enough time |
| Full Stage 4 post-processing | Partially completed | Only BIO repair was tested |
| Hyperparameter tuning / cross-validation | Not completed | Current CRF uses fixed standard parameters |
| Larger annotation adjudication | Not completed | Mention as limitation |

## Final Positioning for Paper

This project should be presented as a pilot-scale legal NER pipeline for U.S. Supreme Court opinions. The main contribution is not a large new corpus, but a complete end-to-end experimental pipeline: data construction, annotation, BIO conversion, rule-based baseline, general-domain baseline, CRF model, span-level evaluation, feature ablation, and error analysis.

The strongest paper claim is:

A domain-trained CRF substantially outperforms both a rule-based extractor and a general-domain pretrained NER system under legal-specific span-level evaluation, but the remaining errors reveal that legal NER is strongly limited by boundary ambiguity and missed PARTY entities.
