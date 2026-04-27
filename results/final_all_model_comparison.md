# Final All-Model Comparison

## Purpose

This file consolidates all final systems and experimental variants into one comparison table. It is intended to serve as the main reference table for the final paper and presentation.

The main evaluation metric is strict span-level exact-match F1. Token-level F1 is also reported when available, but span-level F1 should be treated as the primary NER metric because it requires exact entity boundaries and correct entity type.

## Span-Level Exact-Match Results

| Rank | System | Precision | Recall | F1 | TP | FP | FN | Main Role |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | Tuned CRF | 0.822 | 0.449 | 0.581 | 88 | 19 | 108 | Final best model |
| 2 | CRF + Chunk | 0.802 | 0.454 | 0.580 | 89 | 22 | 107 | Chunk feature experiment |
| 3 | CRF NoStage2 | 0.819 | 0.439 | 0.571 | 86 | 19 | 110 | Rule-output ablation |
| 4 | CRF + Gazetteer | 0.811 | 0.439 | 0.570 | 86 | 20 | 110 | Gazetteer feature experiment |
| 5 | CRF + POS | 0.787 | 0.434 | 0.559 | 85 | 23 | 111 | POS feature experiment |
| 6 | Original CRF | 0.781 | 0.418 | 0.545 | 82 | 23 | 114 | Original legal-domain CRF |
| 7 | CRF + BIO Repair | 0.781 | 0.418 | 0.545 | 82 | 23 | 114 | Minimal post-processing |
| 8 | CRF + Full Post-processing | 0.621 | 0.327 | 0.428 | 64 | 39 | 132 | Full heuristic post-processing |
| 9 | Rule-Based | 0.652 | 0.153 | 0.248 | 30 | 16 | 166 | Rules-only baseline |
| 10 | Stanza | 0.157 | 0.240 | 0.190 | 47 | 252 | 149 | General-domain pretrained baseline |
| 11 | CoNLL-2003 CRF Transfer | 0.087 | 0.061 | 0.072 | 12 | 126 | 184 | Out-of-domain CRF baseline |
| 12 | Majority | 0.000 | 0.000 | 0.000 | 0 | 0 | 68 | Lower-bound baseline |

## Token-Level Results Where Available

| System | Precision | Recall | F1 | Notes |
|---|---:|---:|---:|---|
| Tuned CRF | 0.843 | 0.651 | 0.734 | Final best model |
| CRF + Chunk | 0.845 | 0.638 | 0.727 | Near-tie with tuned CRF |
| CRF + Gazetteer | 0.877 | 0.616 | 0.724 | Higher precision, lower recall |
| CRF NoStage2 | 0.820 | 0.646 | 0.723 | Slightly below tuned CRF |
| CRF + POS | 0.828 | 0.597 | 0.694 | POS features hurt overall |
| Original CRF | 0.803 | 0.601 | 0.688 | Original legal-domain CRF |
| Rule-Based | 0.799 | 0.334 | 0.471 | High precision, low recall |
| Stanza | 0.160 | 0.172 | 0.166 | General-domain mismatch |
| Majority | 0.000 | 0.000 | 0.000 | Predicts no entities |

## Main Findings

### 1. Tuned CRF is the final best model.

The tuned CRF obtains the highest strict span-level F1:

| Model | Span F1 |
|---|---:|
| Tuned CRF | 0.581 |
| Original CRF | 0.545 |

Hyperparameter tuning improves both precision and recall:

| Model | Precision | Recall | F1 |
|---|---:|---:|---:|
| Original CRF | 0.781 | 0.418 | 0.545 |
| Tuned CRF | 0.822 | 0.449 | 0.581 |

Therefore, the tuned CRF should be the final reported system.

### 2. Feature extensions nearly match but do not beat the tuned CRF.

Chunk features nearly tie the tuned CRF:

| Model | Span F1 |
|---|---:|
| Tuned CRF | 0.581 |
| CRF + Chunk | 0.580 |

Gazetteer and POS features do not improve the final result:

| Model | Span F1 |
|---|---:|
| CRF + Gazetteer | 0.570 |
| CRF + POS | 0.559 |

This means the final best system remains the tuned lexical/orthographic/rule-output CRF.

### 3. Removing Stage 2 rule-output features does not improve the final model.

The NoStage2 CRF reaches 0.571 span F1, slightly below the tuned CRF's 0.581. This means the rule-output feature group is not a major driver of performance, but removing it does not improve the final tuned system.

### 4. Full heuristic post-processing hurts performance.

Full Stage 4 post-processing lowers span F1 from 0.545 to 0.428. The Stage 4 ablation shows that this degradation is mainly caused by aggressive span completion. BIO repair, type consistency, and nested resolution alone have no effect.

### 5. Domain transfer is very weak.

The CoNLL-2003 CRF transfer baseline achieves only 0.072 span F1. This confirms that general-domain NER training does not transfer well to legal-specific entity recognition.

### 6. Rule-based extraction is precise but incomplete.

The rule-based system reaches 0.652 precision but only 0.153 recall. This confirms that hand-written legal patterns can identify some reliable entities but cannot cover the full legal NER task.

### 7. Stanza performs poorly under the legal schema.

Stanza achieves only 0.190 span F1. This is expected because general-domain NER systems do not naturally model legal-specific labels such as CITATION, COURT, STATUTE, and JUDGE.

## Paper-Ready Paragraph

Across all systems, the tuned CRF is the strongest model, achieving 0.822 precision, 0.449 recall, and 0.581 strict span-level F1. This improves over the original CRF's 0.545 span-level F1 and substantially outperforms the rule-based baseline, Stanza baseline, and CoNLL-2003 transfer CRF. Additional feature experiments did not surpass the tuned CRF: chunk features nearly matched it with 0.580 F1, gazetteer features reached 0.570 F1, and POS features reached 0.559 F1. The CoNLL-2003 transfer baseline achieved only 0.072 F1, confirming that legal NER requires in-domain annotation and a legal-specific entity schema. Full heuristic post-processing reduced performance to 0.428 F1 because span-completion rules over-expanded entity boundaries. Overall, these experiments show that the best current system is a tuned legal-domain CRF, while the remaining weaknesses are not solved by generic POS, chunk, gazetteer, or post-processing features.

## Presentation Version

Our final best model is the tuned CRF, with 0.581 strict span-level F1. It beats the original CRF, rule-based system, Stanza, and CoNLL transfer baseline. Chunk features almost tie it, but do not beat it. POS and gazetteer features do not improve the overall model. Full post-processing actually hurts because it expands citation spans too aggressively. The main conclusion is that in-domain legal CRF training matters most, while the remaining errors require better legal annotation and better handling of PARTY/CITATION ambiguity.
