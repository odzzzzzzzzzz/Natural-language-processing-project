# CoNLL-2003 Domain-Transfer CRF Baseline

## Motivation

The original project proposal included a CoNLL-2003 domain-transfer baseline. The purpose of this baseline is to test whether a CRF trained on general-domain NER data can transfer to legal-domain NER.

This experiment trains a CRF on CoNLL-2003 and evaluates it directly on the SCOTUS legal NER test set.

## Label Mapping

Because CoNLL-2003 uses a different entity schema, we used the following mapping:

| CoNLL-2003 Label | Legal NER Label |
|---|---|
| PER | PARTY |
| ORG | ORG |
| LOC | O |
| MISC | O |

CoNLL-2003 does not contain legal-specific labels such as CITATION, COURT, STATUTE, JUDGE, or DATE. Therefore, this is intentionally a weak out-of-domain transfer baseline.

## Training Setup

| Item | Value |
|---|---|
| Source training data | CoNLL-2003 |
| Training sentences used | 5000 |
| Model | Linear-chain CRF |
| Features | Lexical, prefix/suffix, orthographic, word-shape, local context |
| Legal test file | data/splits/test.conll |
| Prediction file | data/splits/test_conll2003_crf_pred.conll |
| Saved model | models/conll2003_crf_transfer.pkl |

## Span-Level Results

| Model | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CoNLL2003_CRF | 0.087 | 0.061 | 0.072 | 12 | 126 | 184 |

## Per-Entity Span-Level Results

| Entity Type | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CITATION | 0.000 | 0.000 | 0.000 | 0 | 0 | 37 |
| COURT | 0.000 | 0.000 | 0.000 | 0 | 0 | 29 |
| DATE | 0.000 | 0.000 | 0.000 | 0 | 0 | 23 |
| JUDGE | 0.000 | 0.000 | 0.000 | 0 | 0 | 2 |
| ORG | 0.091 | 0.588 | 0.157 | 10 | 100 | 7 |
| PARTY | 0.071 | 0.023 | 0.035 | 2 | 26 | 85 |
| STATUTE | 0.000 | 0.000 | 0.000 | 0 | 0 | 1 |

## Comparison with Other Systems

| System | Span-Level F1 |
|---|---:|
| Majority | 0.000 |
| CoNLL-2003 CRF Transfer | 0.072 |
| Stanza | 0.190 |
| Rule-Based | 0.248 |
| Legal-Domain CRF | 0.545 |

## Interpretation

The CoNLL-2003 CRF performs very poorly on the legal test set, with span-level F1 of only 0.072. This result confirms the domain-transfer problem: a CRF trained on general-domain news NER data does not learn the entity categories, boundaries, or surface patterns needed for legal text.

The baseline has zero F1 on CITATION, COURT, DATE, JUDGE, and STATUTE because these categories do not exist in CoNLL-2003. It only predicts ORG and PARTY through the approximate ORG -> ORG and PER -> PARTY mappings. Even for these mapped labels, performance is weak: PARTY F1 is only 0.035 and ORG F1 is 0.157.

This result strengthens the main argument of the project: legal NER requires in-domain annotation and legal-specific modeling. The strong gap between CoNLL-2003 CRF transfer F1 = 0.072 and legal-domain CRF F1 = 0.545 shows that the improvement is not simply due to using a CRF architecture, but due to training on legal-domain data with a legal-specific schema.

## Paper-Ready Paragraph

To measure the domain-transfer gap, we trained a CRF on CoNLL-2003 and evaluated it directly on our SCOTUS legal NER test set. We mapped PER to PARTY and ORG to ORG, while mapping LOC and MISC to O because they do not correspond to our legal entity schema. This out-of-domain CRF achieved only 0.072 span-level F1, far below the legal-domain CRF's 0.545. The model failed completely on legal-specific categories such as CITATION, COURT, STATUTE, JUDGE, and DATE, which are absent from CoNLL-2003. This confirms that the performance gain of our CRF comes from in-domain legal annotation and schema design rather than from the CRF architecture alone.
