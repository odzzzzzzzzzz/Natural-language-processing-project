# Legal NER for Supreme Court Opinions

## 1. Overview

We build a multi-stage pipeline for legal named entity recognition (NER) on U.S. Supreme Court opinions. The system combines rule-based methods and a CRF model to extract entities such as CITATION, COURT, DATE, and ORG.

---

## 2. Paragraph-Level Heuristics (Professor Feedback)

We extended our preprocessing pipeline with paragraph-level classification heuristics.

We used:
- Position-based features (first/last paragraphs)
- Discourse connectives (e.g., "however", "therefore")
- Legal cues ("we hold", "the judgment is")
- Jaccard similarity between adjacent paragraphs

Results:
- INTRODUCTION: 538
- BODY: 2249
- CONCLUSION: 133
- 139 candidate paragraph pairs for merging

This confirms that simple positional heuristics are insufficient, and similarity-based merging can capture fragmented legal structures.

---

## 3. Baselines

### Majority baseline

All tokens predicted as O:

- MICRO F1 = 0.000

### Rules-only baseline

| Entity | Precision | Recall | F1 |
|---|---|---|---|
| CITATION | 0.852 | 0.203 | 0.328 |
| DATE | 0.958 | 0.548 | 0.697 |
| MICRO | 0.868 | 0.207 | 0.334 |

---

## 4. CRF Model

We train a linear-chain CRF using:

- Lexical features (n-grams, prefixes, suffixes)
- Orthographic features (capitalization, digits)
- Context features (neighbor tokens)
- Stage 2 rule outputs as features

### Dev performance

- MICRO F1 = 0.786

---

## 5. Test Results

| Model | Precision | Recall | F1 |
|---|---|---|---|
| Rules | 0.868 | 0.207 | 0.334 |
| CRF | 0.867 | 0.283 | 0.427 |

The CRF significantly improves recall while maintaining similar precision.

---

## 6. Ablation Study

| Setting | F1 | Drop |
|---|---|---|
| All features | 0.786 | 0.000 |
| Without lexical | 0.675 | -0.112 |
| Without rules | 0.769 | -0.017 |

Lexical features are most important, while rule-based features provide modest gains.

---

## 7. Error Analysis

Dominant error:

- False negatives (466)

Key observations:

1. Citation fragmentation:
   e.g., "541 U. S. 929" split across tokens or lines

2. Context-dependent entities:
   COURT and ORG require semantic understanding

3. BIO boundary errors:
   Misalignment at punctuation boundaries

4. Type confusion:
   Dates misclassified as citations

5. Paragraph segmentation issues:
   Adjacent fragments should sometimes be merged

---

## 8. Conclusion

Rule-based methods provide high precision but low recall. The CRF improves recall by leveraging contextual features. However, performance is limited by small data size and annotation sparsity.

Future work includes:
- Larger annotated dataset
- Improved ORG detection
- Transformer-based models
- Better paragraph segmentation

