# Error Analysis Summary for Paper

## Main Quantitative Findings

The CRF error analysis shows that false negatives are the dominant source of errors.

| Error Category | Count |
|---|---:|
| False negative | 99 |
| Boundary error | 10 |
| Type error | 7 |
| False positive | 6 |

The largest single error category is missed PARTY entities.

| Error Category | Entity Type | Count |
|---|---|---:|
| False negative | PARTY | 68 |
| False negative | ORG | 14 |
| False negative | CITATION | 12 |
| Type error | CITATION | 5 |
| Boundary error | PARTY | 5 |
| Boundary error | CITATION | 5 |

## Interpretation

The CRF model does not mainly fail by hallucinating entities. Instead, it is conservative and misses many gold entity spans. This explains why the CRF achieves relatively high precision but only moderate recall under span-level evaluation.

PARTY is the most difficult entity type. Although PARTY is frequent in the dataset, many party names appear inside case citations or near citation-like structures. This creates ambiguity between PARTY and CITATION boundaries. For example, in case-name expressions such as "United States v. Booker" or "Hazeltine Research, Inc.", it is difficult to decide whether the model should extract only the party name, the full case name, or the surrounding citation.

CITATION errors are mostly boundary-related. The model often recognizes part of a citation, such as the reporter volume and abbreviation, but fails to include the full reporter string, page number, pinpoint citation, or parenthetical year. This is especially visible in examples such as "379 U.S. 29, 33 (1964)", where the model may predict only "379 U.S. 29".

ORG false negatives suggest that organization names are difficult when they overlap with party names or institutional legal actors. This also explains why general-domain Stanza performs poorly: its ORG predictions do not align well with the legal-specific schema.

The error examples also reveal a possible annotation or alignment issue: some gold spans appear unusually long, sometimes covering a large clause rather than a compact entity. This should be discussed as a limitation of the pilot annotation process and as motivation for stricter annotation guidelines in future work.

## Paper-Ready Paragraph

The error analysis reveals that the CRF's main weakness is recall rather than precision. Among the categorized errors, false negatives are the dominant category, accounting for 99 cases, while boundary errors, type errors, and false positives occur much less frequently. PARTY entities are the largest source of missed predictions, with 68 false negatives. This suggests that the model often fails to recognize legal actors when they appear inside or near citation-like expressions. CITATION errors, by contrast, are often boundary errors: the model may identify part of a reporter citation but fail to include the full page range or parenthetical year. These patterns show that legal NER errors are strongly tied to legal document structure rather than generic named entity ambiguity. The analysis also reveals that some gold spans are unusually long, suggesting that future work should refine the annotation guidelines and perform stronger adjudication before scaling the dataset.
