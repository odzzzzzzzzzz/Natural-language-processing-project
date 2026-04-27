# CRF_Tuned Error Summary for Paper

## Main Error Counts

| Error Category | Count |
|---|---:|
| False negative | 96 |
| False positive | 7 |
| Boundary error | 6 |
| Type error | 6 |

## Most Important Entity-Specific Errors

| Error Type | Entity Type | Count |
|---|---|---:|
| False negative | PARTY | 69 |
| False negative | ORG | 14 |
| False negative | CITATION | 8 |
| False negative | DATE | 5 |
| False positive | CITATION | 5 |
| Boundary error | PARTY | 4 |
| Type error | PARTY | 3 |
| Type error | CITATION | 2 |
| Boundary error | CITATION | 2 |
| Type error | STATUTE | 1 |

## Paper-Ready Interpretation

The final tuned CRF produces 88 correct spans, 19 false positives, and 108 false negatives. The dominant remaining error type is still false negatives, indicating that the model remains conservative even after tuning. PARTY remains the hardest high-frequency entity type, with 69 false negatives. This supports the qualitative conclusion that legal actors are difficult to identify when they appear inside or near citation-like expressions. CITATION errors also remain important: the model has 8 citation false negatives and 2 citation boundary errors. Overall, tuning improves performance, especially for CITATION, but it does not eliminate the core linguistic difficulty of legal NER: exact boundary detection in nested PARTY/CITATION contexts.