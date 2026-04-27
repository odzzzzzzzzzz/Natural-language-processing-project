# Feature Engineering Experiment Summary

## Motivation

The original project plan included several CRF feature groups beyond basic lexical and orthographic features. After establishing the tuned CRF as the strongest baseline model, we tested whether additional feature groups could further improve performance.

The tested feature extensions are:

1. POS features
2. Gazetteer / domain lexicon features
3. Chunk features

All feature-augmented models use the same tuned CRF regularization parameters:

| Parameter | Value |
|---|---:|
| c1 | 0.01 |
| c2 | 0.1 |

Each model was trained on train + dev and evaluated on the held-out test set.

## Overall Feature Comparison

| Model | Token Precision | Token Recall | Token F1 | Span Precision | Span Recall | Span F1 |
|---|---:|---:|---:|---:|---:|---:|
| Tuned CRF | 0.843 | 0.651 | 0.734 | 0.822 | 0.449 | 0.581 |
| CRF + POS | 0.828 | 0.597 | 0.694 | 0.787 | 0.434 | 0.559 |
| CRF + Gazetteer | 0.877 | 0.616 | 0.724 | 0.811 | 0.439 | 0.570 |
| CRF + Chunk | 0.845 | 0.638 | 0.727 | 0.802 | 0.454 | 0.580 |

## Span-Level F1 by Entity Type

| Entity Type | Tuned CRF | CRF + POS | CRF + Gazetteer | CRF + Chunk |
|---|---:|---:|---:|---:|
| CITATION | 0.685 | 0.620 | 0.638 | 0.676 |
| COURT | 0.983 | 0.983 | 0.983 | 0.983 |
| DATE | 0.878 | 0.878 | 0.930 | 0.930 |
| JUDGE | 1.000 | 1.000 | 1.000 | 1.000 |
| ORG | 0.300 | 0.300 | 0.300 | 0.300 |
| PARTY | 0.210 | 0.206 | 0.192 | 0.206 |
| STATUTE | 0.000 | 0.000 | 0.000 | 0.000 |

## Token-Level F1 by Entity Type

| Entity Type | Tuned CRF | CRF + POS | CRF + Gazetteer | CRF + Chunk |
|---|---:|---:|---:|---:|
| CITATION | 0.792 | 0.712 | 0.759 | 0.762 |
| COURT | 0.987 | 0.987 | 0.987 | 0.987 |
| DATE | 0.857 | 0.857 | 0.930 | 0.930 |
| JUDGE | 1.000 | 1.000 | 1.000 | 1.000 |
| ORG | 0.462 | 0.462 | 0.462 | 0.462 |
| PARTY | 0.274 | 0.277 | 0.259 | 0.278 |
| STATUTE | 0.000 | 0.000 | 0.000 | 0.000 |

## Main Findings

### 1. Tuned CRF remains the best overall model.

The tuned CRF achieves the highest span-level F1:

| Model | Span F1 |
|---|---:|
| Tuned CRF | 0.581 |
| CRF + Chunk | 0.580 |
| CRF + Gazetteer | 0.570 |
| CRF + POS | 0.559 |

Although the chunk model nearly matches the tuned CRF, it does not exceed it. Therefore, the tuned CRF remains the final best system.

### 2. POS features do not help.

Adding POS features decreases span-level F1 from 0.581 to 0.559 and token-level F1 from 0.734 to 0.694.

This suggests that general-purpose POS tags do not capture the legal-specific distinctions needed for this task. For example, POS tags can indicate that a token is a proper noun, but they cannot reliably distinguish PARTY, ORG, JUDGE, COURT, or CITATION.

### 3. Gazetteer features help DATE but not the full task.

Gazetteer features improve DATE span-level F1 from 0.878 to 0.930, likely because month names and date-like lexical cues are easy to encode. However, the overall span-level F1 decreases from 0.581 to 0.570.

This suggests that legal lexicons help with surface-regular categories but do not solve harder semantic categories such as PARTY and STATUTE.

### 4. Chunk features nearly match the tuned CRF.

Chunk features achieve span-level F1 of 0.580, almost identical to the tuned CRF's 0.581. They improve DATE span-level F1 to 0.930, but they do not improve PARTY or STATUTE.

This suggests that shallow phrase-structure information is not harmful, but it does not solve the main legal-semantic ambiguity in the dataset.

### 5. PARTY and STATUTE remain unresolved.

Across all feature variants, PARTY remains weak and STATUTE remains zero. This means the main remaining errors are not solved by adding generic linguistic features. They likely require:

- more annotated examples,
- clearer annotation guidelines,
- better treatment of nested PARTY/CITATION structures,
- legal-specific gazetteers built from case metadata,
- or a model that can represent overlapping entities.

## Paper-Ready Paragraph

We tested three additional feature extensions beyond the tuned CRF: POS features, gazetteer features, and chunk features. None of these feature groups improved the overall final result. POS features reduced span-level F1 from 0.581 to 0.559, suggesting that general-purpose syntactic categories do not capture the legal-specific distinctions required by the task. Gazetteer features improved DATE recognition, raising DATE span-level F1 from 0.878 to 0.930, but overall span-level F1 decreased to 0.570. Chunk features nearly matched the tuned CRF, achieving 0.580 span-level F1, but they did not surpass it. Across all feature variants, PARTY and STATUTE remained difficult. This indicates that the main remaining errors are not simply due to missing POS, chunk, or lexicon features, but instead reflect deeper legal-semantic ambiguity and limited training data for difficult entity types.

## Presentation Version

We also tested three extra feature groups: POS, gazetteer, and chunk features. None of them beat the tuned CRF. POS hurt performance, gazetteers helped DATE but not the full task, and chunk features almost tied the tuned CRF. The important takeaway is that generic linguistic features do not solve the hardest legal labels. PARTY and STATUTE remain difficult because they require legal-semantic understanding and better annotation coverage.
