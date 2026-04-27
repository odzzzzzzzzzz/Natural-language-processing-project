# Final Claims Checklist

This checklist records what we can safely claim in the final paper and presentation, and what should be framed as limitation or future work.

## Safe Claims

### 1. We built an end-to-end pilot legal NER pipeline.

This is safe to claim because the repository contains the complete workflow:

- data construction
- annotation preparation
- Label Studio export conversion
- train/dev/test split
- majority baseline
- rule-based baseline
- Stanza baseline
- CRF model
- token-level evaluation
- span-level exact-match evaluation
- BIO repair post-processing
- CRF feature ablation
- error analysis
- final evaluation wrapper

Recommended wording:

> We present a pilot-scale end-to-end legal NER pipeline for U.S. Supreme Court opinions.

---

### 2. The CRF outperforms all implemented baselines.

This is safe to claim because the final results show:

| System | Token F1 | Span F1 |
|---|---:|---:|
| Majority | 0.000 | 0.000 |
| Stanza | 0.166 | 0.190 |
| Rule-Based | 0.471 | 0.248 |
| CRF | 0.688 | 0.545 |

Recommended wording:

> The CRF achieves the strongest performance among all implemented systems, with token-level F1 of 0.688 and strict span-level F1 of 0.545.

---

### 3. COURT and DATE are the strongest entity types.

This is safe to claim because CRF span-level F1 is:

| Entity | CRF Span F1 |
|---|---:|
| COURT | 0.983 |
| DATE | 0.905 |

Recommended wording:

> The CRF performs especially well on COURT and DATE, likely because these entities have stable surface forms and strong contextual cues.

---

### 4. PARTY is the main weakness.

This is safe to claim because PARTY has low span-level F1 and dominates false negatives.

| Entity | CRF Span F1 |
|---|---:|
| PARTY | 0.192 |

Error analysis:

| Error Category | Entity Type | Count |
|---|---|---:|
| False negative | PARTY | 68 |

Recommended wording:

> PARTY is the most difficult high-frequency entity type, largely because party names often appear inside or near citation-like structures.

---

### 5. False negatives are the dominant CRF error type.

This is safe to claim because error analysis shows:

| Error Category | Count |
|---|---:|
| False negative | 99 |
| Boundary error | 10 |
| Type error | 7 |
| False positive | 6 |

Recommended wording:

> The CRF is conservative: it misses many gold spans rather than hallucinating many false entities.

---

### 6. Stage 2 rule features hurt the CRF in the current implementation.

This is safe to claim because ablation shows:

| Setting | Dev Micro-F1 |
|---|---:|
| All features | 0.509 |
| Without Group F | 0.549 |

Recommended wording:

> Removing the rule-output feature group improves development F1, suggesting that naive rule-feature integration introduces noise.

Do not write that Stage 2 features improve the CRF.

---

### 7. BIO repair did not improve results.

This is safe to claim because:

| System | Span F1 |
|---|---:|
| CRF | 0.545 |
| CRF + BIO Repair | 0.545 |

Recommended wording:

> BIO repair has no effect on final span-level F1, showing that the main CRF errors are not invalid BIO transitions.

---

## Claims to Avoid

### 1. Do not claim a full 800-1000 passage corpus.

Actual status:

- 150 passages annotated
- 133 usable passage/sentence groups with at least one entity
- 3,245 entity spans

Use instead:

> pilot-scale corpus

---

### 2. Do not claim valid IAA.

Actual status:

- 50-passage pilot set was annotated by Yulong
- 150-passage expanded corpus was annotated by Guyu
- These two sets do not overlap

Use instead:

> annotation provenance

Do not report Cohen's kappa or pairwise annotator F1 unless a second annotator completes the same 50 passages.

---

### 3. Do not claim full Stage 4 post-processing.

Actual status:

- BIO repair implemented
- span completion not implemented
- type consistency voting not implemented
- nested entity resolution not implemented

Use instead:

> We tested a minimal BIO repair post-processing step.

---

### 4. Do not claim full CRF feature groups A-G.

Actual status:

Implemented:

- Group A: lexical/contextual
- Group B: orthographic
- Group F: rule-output
- Group G: boundary

Not implemented in final model:

- Group C: POS
- Group D: chunk
- Group E: gazetteer

Use instead:

> The final CRF uses four feature groups: lexical/contextual, orthographic, rule-output, and boundary features.

---

### 5. Do not claim CoNLL-2003 domain-transfer baseline.

Actual status:

- Majority baseline implemented
- Rule-based baseline implemented
- Stanza baseline implemented
- Legal-domain CRF implemented
- CoNLL-2003-trained CRF not implemented

Use instead:

> A CoNLL-2003 transfer baseline remains future work.

---

### 6. Do not claim hyperparameter tuning or 10-fold CV.

Actual status:

- Fixed CRF parameters: c1=0.1, c2=0.1
- Ablation completed
- Cross-validation tuning not completed

Use instead:

> The CRF uses fixed standard regularization parameters; systematic hyperparameter tuning remains future work.

---

### 7. Do not overinterpret STATUTE and JUDGE.

Actual test counts:

| Entity | Test Count |
|---|---:|
| STATUTE | 1 |
| JUDGE | 2 |

Use instead:

> STATUTE and JUDGE results are unstable because the test set contains very few examples of these categories.

---

## Mandatory Disclosure Sentences for Presentation

Use these sentences directly if needed.

1. Corpus size:

> We originally targeted 800-1000 passages, but completed 150 annotated passages, so we frame this as a pilot-scale study.

2. IAA:

> Our annotation files show contribution from multiple annotators, but the shared overlapping annotation needed for true IAA was not completed.

3. Feature groups:

> We implemented four CRF feature groups: lexical/contextual, orthographic, rule-output, and boundary features. POS, chunk, and gazetteer features remain future work.

4. Rare labels:

> STATUTE and JUDGE have very small test counts, so we do not overinterpret those per-type F1 scores.

5. Stage 2:

> The rule-based system is useful as a standalone high-precision baseline, but its direct use as a CRF feature introduced noise in this implementation.

## Final One-Sentence Framing

> This project should be presented as a pilot-scale legal NER pipeline that successfully implements the full experimental infrastructure and identifies the central linguistic error patterns, rather than as a final large-scale legal NER benchmark.
