# Final All-Model Comparison

## Purpose

This file consolidates all final systems and experimental variants into one comparison table. It is intended to serve as the main reference table for the final paper and presentation.

The primary evaluation metric is strict span-level exact-match F1. Token-level F1 is also reported when available, but span-level F1 should be treated as the main NER metric because it requires exact entity boundaries and correct entity type.

## Span-Level Exact-Match Results

| Rank | System | Precision | Recall | F1 | TP | FP | FN | Main Role |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | Tuned CRF | 0.822 | 0.449 | 0.581 | 88 | 19 | 108 | Final best model |
| 2 | CRF + Chunk | 0.802 | 0.454 | 0.580 | 89 | 22 | 107 | Chunk feature experiment |
| 3 | Ensemble TunedRule | 0.793 | 0.449 | 0.573 | 88 | 23 | 108 | Rule-CRF ensemble |
| 4 | CRF NoStage2 | 0.819 | 0.439 | 0.571 | 86 | 19 | 110 | Rule-output ablation |
| 5 | CRF + Gazetteer | 0.811 | 0.439 | 0.570 | 86 | 20 | 110 | Gazetteer feature experiment |
| 6 | Ensemble NoStage2Rule | 0.782 | 0.439 | 0.562 | 86 | 24 | 110 | NoStage2 + rule ensemble |
| 7 | CRF + POS | 0.787 | 0.434 | 0.559 | 85 | 23 | 111 | POS feature experiment |
| 8 | CRF + WordCluster | 0.780 | 0.434 | 0.557 | 85 | 24 | 111 | Brown-style word-cluster experiment |
| 9 | Original CRF | 0.781 | 0.418 | 0.545 | 82 | 23 | 114 | Original legal-domain CRF |
| 10 | CRF + BIO Repair | 0.781 | 0.418 | 0.545 | 82 | 23 | 114 | Minimal post-processing |
| 11 | CRF + Full Post-processing | 0.621 | 0.327 | 0.428 | 64 | 39 | 132 | Full heuristic post-processing |
| 12 | Rule-Based | 0.652 | 0.153 | 0.248 | 30 | 16 | 166 | Rules-only baseline |
| 13 | Stanza | 0.157 | 0.240 | 0.190 | 47 | 252 | 149 | General-domain pretrained baseline |
| 14 | CoNLL-2003 CRF Transfer | 0.087 | 0.061 | 0.072 | 12 | 126 | 184 | Out-of-domain CRF baseline |
| 15 | Majority | 0.000 | 0.000 | 0.000 | 0 | 0 | 68 | Lower-bound baseline |

## Token-Level Results Where Available

| System | Precision | Recall | F1 | Notes |
|---|---:|---:|---:|---|
| Tuned CRF | 0.843 | 0.651 | 0.734 | Final best model |
| Ensemble TunedRule | 0.819 | 0.662 | 0.732 | Slightly higher recall, lower precision |
| CRF + Chunk | 0.845 | 0.638 | 0.727 | Near-tie with tuned CRF |
| Ensemble NoStage2Rule | 0.800 | 0.664 | 0.726 | Rule ensemble variant |
| CRF + Gazetteer | 0.877 | 0.616 | 0.724 | Higher precision, lower recall |
| CRF NoStage2 | 0.820 | 0.646 | 0.723 | Slightly below tuned CRF |
| CRF + WordCluster | 0.821 | 0.613 | 0.702 | Brown-style word-cluster features |
| CRF + POS | 0.828 | 0.597 | 0.694 | POS features hurt overall |
| Original CRF | 0.803 | 0.601 | 0.688 | Original legal-domain CRF |
| Rule-Based | 0.799 | 0.334 | 0.471 | High precision, low recall |
| Stanza | 0.160 | 0.172 | 0.166 | General-domain mismatch |
| Majority | 0.000 | 0.000 | 0.000 | Predicts no entities |

## Main Findings

### 1. Tuned CRF remains the final best model.

The tuned CRF obtains the highest strict span-level F1:

| Model | Span F1 |
|---|---:|
| Tuned CRF | 0.581 |
| CRF + Chunk | 0.580 |
| Ensemble TunedRule | 0.573 |
| CRF NoStage2 | 0.571 |
| CRF + Gazetteer | 0.570 |

Although several variants are close, none surpass the tuned CRF. Therefore, the tuned CRF remains the final reported system.

### 2. Hyperparameter tuning is the most useful improvement.

The original CRF achieved 0.545 span-level F1. After dev-set tuning and retraining on train + dev, the tuned CRF reached 0.581 span-level F1.

| Model | Precision | Recall | F1 |
|---|---:|---:|---:|
| Original CRF | 0.781 | 0.418 | 0.545 |
| Tuned CRF | 0.822 | 0.449 | 0.581 |

### 3. Feature extensions do not beat the tuned CRF.

POS, gazetteer, chunk, and word-cluster features were tested. Chunk features nearly tie the tuned CRF, but none of the extra feature groups improve the final result.

| Feature Variant | Span F1 |
|---|---:|
| CRF + Chunk | 0.580 |
| CRF + Gazetteer | 0.570 |
| CRF + POS | 0.559 |
| CRF + WordCluster | 0.557 |

### 4. Ensemble systems do not improve strict span-level F1.

The rule-CRF ensemble recovers a few additional rule-based spans, especially citation-like spans, but it also introduces boundary and precision noise.

| Ensemble Variant | Span F1 |
|---|---:|
| Tuned CRF | 0.581 |
| Ensemble TunedRule | 0.573 |
| Ensemble NoStage2Rule | 0.562 |

### 5. Full heuristic post-processing hurts performance.

Full Stage 4 post-processing lowers span-level F1 from 0.545 to 0.428. The Stage 4 ablation shows that this degradation is mainly caused by aggressive span completion. BIO repair, type consistency, and nested resolution alone have no effect.

### 6. Domain transfer is very weak.

The CoNLL-2003 CRF transfer baseline achieves only 0.072 span-level F1. This confirms that general-domain NER training does not transfer well to legal-specific entity recognition.

### 7. Rule-based extraction is precise but incomplete.

The rule-based system reaches 0.652 precision but only 0.153 recall. This confirms that hand-written legal patterns can identify some reliable entities but cannot cover the full legal NER task.

## Paper-Ready Paragraph

Across all systems, the tuned CRF is the strongest model, achieving 0.822 precision, 0.449 recall, and 0.581 strict span-level F1. This improves over the original CRF's 0.545 span-level F1 and substantially outperforms the rule-based baseline, Stanza baseline, and CoNLL-2003 transfer CRF. Additional feature experiments did not surpass the tuned CRF: chunk features nearly matched it with 0.580 F1, gazetteer features reached 0.570 F1, POS features reached 0.559 F1, and Brown-style word-cluster features reached 0.557 F1. Two rule-CRF ensemble variants also failed to improve the final result, achieving 0.573 and 0.562 F1. The CoNLL-2003 transfer baseline achieved only 0.072 F1, confirming that legal NER requires in-domain annotation and a legal-specific entity schema. Overall, these experiments show that the best current system is a tuned legal-domain CRF, while the remaining weaknesses are not solved by generic POS, chunk, gazetteer, word-cluster, ensemble, or post-processing features.

## Presentation Version

Our final best model is the tuned CRF, with 0.581 strict span-level F1. It beats the original CRF, rule-based system, Stanza, and CoNLL transfer baseline. Chunk features almost tie it, but do not beat it. POS, gazetteer, word-cluster, and ensemble variants do not improve the overall result. Full post-processing actually hurts because it expands citation spans too aggressively. The main conclusion is that in-domain legal CRF training and tuning matter most, while the remaining errors require better legal annotation and better handling of PARTY/CITATION ambiguity.
