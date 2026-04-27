# CRF Feature Ablation Summary

## Ablation Results

| Setting | Disabled Group | Dev Micro-F1 | F1 Drop |
|---|---:|---:|---:|
| All features |  | 0.509 | 0.000 |
| Without group A | A | 0.380 | 0.129 |
| Without group B | B | 0.470 | 0.039 |
| Without group F | F | 0.549 | -0.040 |
| Without group G | G | 0.508 | 0.001 |

## Feature Group Meanings

| Group | Meaning |
|---|---|
| A | Lexical and local context features, including token identity, prefixes, suffixes, previous words, and next words |
| B | Orthographic features, including capitalization, digits, punctuation, section symbols, and word shape |
| F | Stage 2 rule-based prediction features |
| G | Sentence boundary features, including beginning-of-sentence and end-of-sentence indicators |

## Interpretation

The ablation study shows that lexical and contextual features are the most important feature group for the CRF. Removing Group A causes the largest drop in development micro-F1, from 0.509 to 0.380. This indicates that token identity, prefixes, suffixes, and neighboring words provide the strongest signal for recognizing legal entities.

Orthographic features also help, but to a smaller degree. Removing Group B reduces development F1 from 0.509 to 0.470. This is expected because legal text contains many capitalization patterns, digits, punctuation marks, and citation-like forms that are informative for CITATION, DATE, COURT, and STATUTE recognition.

Removing Group G has almost no effect, suggesting that simple sentence-boundary indicators are not very useful for this dataset.

Interestingly, removing Group F, the Stage 2 rule-based feature group, improves development F1 from 0.509 to 0.549. This suggests that the current rule-based predictions do not reliably help the CRF and may introduce noisy or overly sparse signals. Therefore, although rule-based extraction is useful as an independent baseline, its output should be integrated more carefully if used as a CRF feature.

## Paper-Ready Paragraph

Feature ablation shows that the CRF relies most heavily on lexical and local contextual features. Removing Group A, which includes token identity, prefixes, suffixes, and neighboring words, causes the largest F1 drop, from 0.509 to 0.380. Orthographic features also contribute positively, reflecting the importance of capitalization, digits, punctuation, and word-shape patterns in legal text. Sentence-boundary features have almost no effect. Surprisingly, removing the Stage 2 rule-based prediction features improves development F1, suggesting that the current rule output may introduce noisy signals when used directly as CRF input. This indicates that rule-based extraction is useful as a standalone high-precision baseline, but future work should explore more careful ways of integrating rule confidence into statistical sequence labeling.
