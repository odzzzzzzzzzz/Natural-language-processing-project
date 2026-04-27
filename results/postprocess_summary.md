# Post-processing Experiment

## BIO Repair

We applied a simple BIO repair rule to the CRF predictions:

1. If an `I-X` tag appears after `O`, it is converted to `B-X`.
2. If an `I-X` tag appears after a different entity type, it is converted to `B-X`.

## Results

| System | Precision | Recall | F1 |
|---|---:|---:|---:|
| CRF | 0.781 | 0.418 | 0.545 |
| CRF + BIO Repair | 0.781 | 0.418 | 0.545 |

## Interpretation

BIO repair did not change the final span-level score. This suggests that the CRF's main errors are not caused by invalid BIO transitions. Instead, the main remaining issues are false negatives, boundary mismatches, and entity-type ambiguity, especially for PARTY and CITATION entities.
