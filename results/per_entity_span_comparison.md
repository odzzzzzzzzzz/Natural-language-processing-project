# Per-Entity Span-Level F1 Comparison

| Entity Type | Rule-Based F1 | Stanza F1 | CRF F1 |
|---|---:|---:|---:|
| CITATION | 0.424 | 0.000 | 0.571 |
| COURT | 0.000 | 0.000 | 0.983 |
| DATE | 0.800 | 0.415 | 0.905 |
| JUDGE | 0.000 | 0.000 | 0.667 |
| ORG | 0.000 | 0.144 | 0.300 |
| PARTY | 0.000 | 0.239 | 0.192 |
| STATUTE | 0.000 | 0.000 | 0.000 |

## Key Observations

The CRF performs best on COURT and DATE, suggesting that these categories have relatively stable surface patterns and sufficient contextual cues.

CITATION remains challenging even for the CRF, because legal citations appear in many formats and often include punctuation-heavy structures.

PARTY has low CRF F1 despite being frequent in the dataset, suggesting that party names are difficult because of boundary ambiguity, nesting inside citations, and overlap with organization names.

STATUTE and JUDGE results should be interpreted cautiously because the test set contains very few examples of these categories.
