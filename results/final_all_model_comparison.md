# Final All-Model Comparison

## Purpose

This file consolidates all final systems and experimental variants into one comparison table. The primary evaluation metric is strict span-level exact-match F1.

## Span-Level Exact-Match Results

| Rank | System | Precision | Recall | F1 | TP | FP | FN | Main Role |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | Tuned CRF | 0.822 | 0.449 | 0.581 | 88 | 19 | 108 | Final best model |
| 2 | CRF + Chunk | 0.802 | 0.454 | 0.580 | 89 | 22 | 107 | Chunk feature experiment |
| 3 | Ensemble TunedRule | 0.793 | 0.449 | 0.573 | 88 | 23 | 108 | Rule-CRF ensemble |
| 4 | CRF NoStage2 | 0.819 | 0.439 | 0.571 | 86 | 19 | 110 | Rule-output ablation |
| 5 | CRF + Gazetteer | 0.811 | 0.439 | 0.570 | 86 | 20 | 110 | Gazetteer feature experiment |
| 6 | CRF CVSelected | 0.804 | 0.439 | 0.568 | 86 | 21 | 110 | 10-fold CV-selected CRF |
| 7 | Ensemble NoStage2Rule | 0.782 | 0.439 | 0.562 | 86 | 24 | 110 | NoStage2 + rule ensemble |
| 8 | CRF + POS | 0.787 | 0.434 | 0.559 | 85 | 23 | 111 | POS feature experiment |
| 9 | CRF + WordCluster | 0.780 | 0.434 | 0.557 | 85 | 24 | 111 | Brown-style word-cluster experiment |
| 10 | Original CRF | 0.781 | 0.418 | 0.545 | 82 | 23 | 114 | Original legal-domain CRF |
| 11 | CRF + BIO Repair | 0.781 | 0.418 | 0.545 | 82 | 23 | 114 | Minimal post-processing |
| 12 | CRF + Full Post-processing | 0.621 | 0.327 | 0.428 | 64 | 39 | 132 | Full heuristic post-processing |
| 13 | Rule-Based | 0.652 | 0.153 | 0.248 | 30 | 16 | 166 | Rules-only baseline |
| 14 | Stanza | 0.157 | 0.240 | 0.190 | 47 | 252 | 149 | General-domain pretrained baseline |
| 15 | CoNLL-2003 CRF Transfer | 0.087 | 0.061 | 0.072 | 12 | 126 | 184 | Out-of-domain CRF baseline |
| 16 | Majority | 0.000 | 0.000 | 0.000 | 0 | 0 | 68 | Lower-bound baseline |

## Token-Level Results Where Available

| System | Precision | Recall | F1 | Notes |
|---|---:|---:|---:|---|
| Tuned CRF | 0.843 | 0.651 | 0.734 | Final best model |
| Ensemble TunedRule | 0.819 | 0.662 | 0.732 | Slightly higher recall, lower precision |
| CRF CVSelected | 0.865 | 0.634 | 0.732 | CV-selected regularization |
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

The tuned CRF remains the final best model. Although 10-fold cross-validation selected `c1=0.1, c2=0.1`, the CV-selected model reached only 0.568 span-level F1 on the held-out test set, below the dev-selected tuned CRF's 0.581. Therefore, the final reported model remains the dev-selected tuned CRF.

Feature extensions and enhanced systems did not surpass the tuned CRF. Chunk features nearly tied it with 0.580 span F1, but POS, gazetteer, word-cluster, ensemble, NoStage2, and full post-processing variants all remained lower.

The CoNLL-2003 transfer baseline achieved only 0.072 span F1, confirming that legal NER requires in-domain annotation and a legal-specific schema.

## Paper-Ready Paragraph

Across all systems, the dev-selected tuned CRF is the strongest model, achieving 0.822 precision, 0.449 recall, and 0.581 strict span-level F1. We additionally performed a 10-fold cross-validation tuning check, which selected c1=0.1 and c2=0.1 with mean CV F1 of 0.602. However, when retrained on train plus development data and evaluated on the held-out test set, this CV-selected model achieved only 0.568 span-level F1. Therefore, we retain the dev-selected tuned CRF as the final reported system. Additional feature experiments did not surpass the tuned CRF: chunk features nearly matched it with 0.580 F1, gazetteer features reached 0.570 F1, POS features reached 0.559 F1, and Brown-style word-cluster features reached 0.557 F1. Rule-CRF ensemble variants also failed to improve the final result. These experiments show that in-domain legal CRF training and careful tuning matter most, while the remaining weaknesses require better legal annotation and better handling of PARTY/CITATION ambiguity.

## Presentation Version

Our final best model is still the dev-selected tuned CRF, with 0.581 strict span F1. We also ran 10-fold CV; it selected a slightly different parameter setting, but that model only got 0.568 on the held-out test set. So CV confirms that tuning matters, but it does not replace our final model. None of the extra features or ensemble systems beat the tuned CRF.
