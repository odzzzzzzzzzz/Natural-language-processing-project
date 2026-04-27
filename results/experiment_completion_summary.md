# Final Experiment Completion Summary

## Project Status

This project is now a complete pilot-scale legal NER experiment pipeline for U.S. Supreme Court opinions.

The final best-performing model is:

| Final Best System | Token F1 | Span Precision | Span Recall | Span F1 |
|---|---:|---:|---:|---:|
| Tuned CRF | 0.734 | 0.822 | 0.449 | 0.581 |

The primary evaluation metric is strict span-level exact-match F1.

## Completed Core Pipeline

| Component | Status | Output Files |
|---|---|---|
| Dataset construction | Completed | data/annotated/, data/splits/ |
| Train/dev/test split | Completed | data/splits/train.conll, dev.conll, test.conll |
| Dataset statistics | Completed | results/dataset_stats.md |
| Majority baseline | Completed | results/span_eval_Majority.md |
| Rule-based baseline | Completed | results/span_eval_RuleBased.md |
| Stanza baseline | Completed | results/span_eval_Stanza.md |
| Original CRF | Completed | results/span_eval_CRF.md |
| Tuned CRF | Completed | results/span_eval_CRF_Tuned.md |
| Token-level evaluation | Completed | results/token_eval_results.md |
| Span-level evaluation | Completed | results/main_results.md |
| Final evaluation wrapper | Completed | src/evaluation/run_final_eval.py |

## Completed Additional Experiments

### 1. CoNLL-2003 Domain Transfer Baseline

| System | Span F1 |
|---|---:|
| CoNLL-2003 CRF Transfer | 0.072 |

Completed files:

- src/baselines/conll2003_crf_baseline.py
- data/splits/test_conll2003_crf_pred.conll
- models/conll2003_crf_transfer.pkl
- results/conll2003_transfer_summary.md
- results/span_eval_CoNLL2003_CRF.md

Main conclusion:

The CoNLL-2003 CRF transfer baseline performs very poorly on legal NER, confirming that general-domain NER does not transfer well to legal-specific labels such as CITATION, COURT, STATUTE, JUDGE, and PARTY.

### 2. CRF Hyperparameter Tuning

| Model | Span F1 |
|---|---:|
| Original CRF | 0.545 |
| Tuned CRF | 0.581 |

Completed files:

- src/stage3_crf/tune_crf.py
- models/crf_tuned.pkl
- data/splits/test_crf_tuned_pred.conll
- results/crf_tuning.csv
- results/crf_tuning.md
- results/crf_tuning_summary_for_paper.md
- results/span_eval_CRF_Tuned.md

Main conclusion:

Development-set tuning over c1 and c2 improved final span-level F1 from 0.545 to 0.581. This is the strongest positive experimental improvement in the project.

### 3. Stage 4 Post-processing

| System | Span F1 |
|---|---:|
| Original CRF | 0.545 |
| CRF + BIO Repair | 0.545 |
| CRF + Full Post-processing | 0.428 |

Completed files:

- src/stage4_postprocess/simple_bio_repair.py
- src/stage4_postprocess/postprocess.py
- src/stage4_postprocess/postprocess_ablation.py
- results/postprocess_summary.md
- results/full_postprocess_summary.md
- results/postprocess_ablation_summary.md
- results/span_eval_CRF_BIO_Repair.md
- results/span_eval_CRF_FullPostprocess.md

Main conclusion:

BIO repair had no effect. Full heuristic post-processing hurt performance because span-completion rules over-expanded legal citation boundaries.

### 4. POS Feature Experiment

| Model | Span F1 | Token F1 |
|---|---:|---:|
| Tuned CRF | 0.581 | 0.734 |
| CRF + POS | 0.559 | 0.694 |

Completed files:

- src/stage3_crf/train_crf_pos.py
- data/splits/test_crf_pos_pred.conll
- models/crf_pos.pkl
- results/pos_feature_summary.md
- results/span_eval_CRF_POS.md
- results/token_eval_CRF_POS.md

Main conclusion:

POS features did not help. General-purpose syntactic categories do not directly encode legal-specific distinctions such as CITATION, PARTY, COURT, and STATUTE.

### 5. Gazetteer Feature Experiment

| Model | Span F1 | Token F1 |
|---|---:|---:|
| Tuned CRF | 0.581 | 0.734 |
| CRF + Gazetteer | 0.570 | 0.724 |

Completed files:

- src/stage3_crf/train_crf_gazetteer.py
- data/splits/test_crf_gazetteer_pred.conll
- models/crf_gazetteer.pkl
- results/gazetteer_feature_summary.md
- results/span_eval_CRF_Gazetteer.md
- results/token_eval_CRF_Gazetteer.md

Main conclusion:

Gazetteer features helped DATE recognition but did not improve the overall model. Legal lexicons alone do not solve PARTY and STATUTE errors.

### 6. Chunk Feature Experiment

| Model | Span F1 | Token F1 |
|---|---:|---:|
| Tuned CRF | 0.581 | 0.734 |
| CRF + Chunk | 0.580 | 0.727 |

Completed files:

- src/stage3_crf/train_crf_chunk.py
- data/splits/test_crf_chunk_pred.conll
- models/crf_chunk.pkl
- results/chunk_feature_summary.md
- results/span_eval_CRF_Chunk.md
- results/token_eval_CRF_Chunk.md

Main conclusion:

Chunk features nearly tied the tuned CRF but did not surpass it. Shallow phrase-structure information is not enough to solve the main legal-semantic ambiguity.

### 7. NoStage2 / No Rule-Output Feature Experiment

| Model | Span F1 | Token F1 |
|---|---:|---:|
| Tuned CRF | 0.581 | 0.734 |
| CRF NoStage2 | 0.571 | 0.723 |

Completed files:

- src/stage3_crf/train_crf_no_stage2.py
- data/splits/test_crf_no_stage2_pred.conll
- models/crf_no_stage2.pkl
- results/no_stage2_feature_summary.md
- results/span_eval_CRF_NoStage2.md
- results/token_eval_CRF_NoStage2.md

Main conclusion:

Removing Stage 2 rule-output features did not improve the final model. The rule-output feature is not the main source of performance, but removing it slightly lowers final F1.

### 8. Word-Cluster Feature Experiment

| Model | Span F1 | Token F1 |
|---|---:|---:|
| Tuned CRF | 0.581 | 0.734 |
| CRF + WordCluster | 0.557 | 0.702 |

Completed files:

- src/stage3_crf/train_crf_wordcluster.py
- data/splits/test_crf_wordcluster_pred.conll
- models/crf_wordcluster.pkl
- models/word_clusters.json
- results/wordcluster_feature_summary.md
- results/span_eval_CRF_WordCluster.md
- results/token_eval_CRF_WordCluster.md

Main conclusion:

Brown-style distributional word-cluster features did not help. The pilot corpus is likely too small for stable clusters, and the hardest labels require legal-semantic distinctions rather than only distributional similarity.

### 9. Rule-CRF Ensemble Experiment

| Model | Span F1 | Token F1 |
|---|---:|---:|
| Tuned CRF | 0.581 | 0.734 |
| Ensemble TunedRule | 0.573 | 0.732 |
| Ensemble NoStage2Rule | 0.562 | 0.726 |

Completed files:

- src/stage3_crf/ensemble.py
- data/splits/test_ensemble_tuned_rule_pred.conll
- data/splits/test_ensemble_nostage2_rule_pred.conll
- results/ensemble_summary.md
- results/span_eval_Ensemble_TunedRule.md
- results/token_eval_Ensemble_TunedRule.md
- results/span_eval_Ensemble_NoStage2Rule.md
- results/token_eval_Ensemble_NoStage2Rule.md

Main conclusion:

The ensemble recovered a few additional rule-based spans but did not improve strict span-level F1. Rule predictions introduced enough boundary or precision noise that the tuned CRF remained better.

### 10. Tuned CRF Error Analysis

Completed files:

- src/evaluation/error_analysis_any.py
- results/error_analysis/crf_tuned_errors.md
- results/error_analysis/crf_tuned_error_summary_for_paper.md
- results/error_analysis/error_comparison_original_vs_tuned.md

Main conclusion:

Tuning improved the original CRF by reducing boundary errors and improving CITATION, but PARTY remains the dominant source of false negatives.

## Final All-Model Ranking

| Rank | System | Span F1 |
|---:|---|---:|
| 1 | Tuned CRF | 0.581 |
| 2 | CRF + Chunk | 0.580 |
| 3 | Ensemble TunedRule | 0.573 |
| 4 | CRF NoStage2 | 0.571 |
| 5 | CRF + Gazetteer | 0.570 |
| 6 | Ensemble NoStage2Rule | 0.562 |
| 7 | CRF + POS | 0.559 |
| 8 | CRF + WordCluster | 0.557 |
| 9 | Original CRF | 0.545 |
| 10 | CRF + BIO Repair | 0.545 |
| 11 | CRF + Full Post-processing | 0.428 |
| 12 | Rule-Based | 0.248 |
| 13 | Stanza | 0.190 |
| 14 | CoNLL-2003 CRF Transfer | 0.072 |
| 15 | Majority | 0.000 |

## Remaining Incomplete Component

### True IAA / Adjudication

This remains incomplete.

Current status:

- 50-passage pilot set was annotated by Yulong.
- 150-passage expanded set was annotated by Guyu.
- These two sets do not overlap.
- Therefore, true inter-annotator agreement cannot yet be computed.

Needed to complete IAA:

1. Give the clean 50-passage Label Studio import file to another annotator.
2. Have them independently annotate the exact same 50 passages.
3. Export their JSON file.
4. Convert it to CoNLL.
5. Compute token-level agreement and span-level annotator F1.
6. Optionally adjudicate disagreements into a final gold IAA file.

Recommended wording:

> We report annotation provenance, but true inter-annotator agreement remains future work because the independently annotated files do not yet cover the same text.

## Final Paper Framing

The project should be framed as:

> a complete pilot-scale legal NER pipeline for U.S. Supreme Court opinions.

The project should not be framed as:

> a large fully adjudicated legal NER benchmark.

## Final Takeaway

Except for true IAA/adjudication, the major experimental gaps from the original plan have now been addressed. The final experimental story is coherent:

1. General-domain NER transfer is weak.
2. Rules are precise but incomplete.
3. Legal-domain CRF training is much stronger.
4. Hyperparameter tuning gives the strongest improvement.
5. Extra POS, chunk, gazetteer, word-cluster, ensemble, and post-processing experiments do not beat the tuned CRF.
6. The remaining core challenge is PARTY/CITATION ambiguity under a flat BIO schema.
