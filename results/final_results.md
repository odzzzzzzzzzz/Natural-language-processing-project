# Final Evaluation Results

## Rules-only baseline on test set

| Entity Type | Precision | Recall | F1 |
|---|---:|---:|---:|
| CITATION | 0.852 | 0.203 | 0.328 |
| COURT | 0.000 | 0.000 | 0.000 |
| DATE | 0.958 | 0.548 | 0.697 |
| ORG | 0.000 | 0.000 | 0.000 |
| MICRO | 0.868 | 0.207 | 0.334 |

## CRF model on test set

| Entity Type | Precision | Recall | F1 |
|---|---:|---:|---:|
| CITATION | 0.875 | 0.284 | 0.429 |
| COURT | 0.762 | 0.457 | 0.571 |
| DATE | 0.923 | 0.286 | 0.436 |
| ORG | 0.000 | 0.000 | 0.000 |
| MICRO | 0.867 | 0.283 | 0.427 |

## Summary

The CRF improves over the rules-only baseline mainly by increasing recall while maintaining nearly the same precision. The micro-F1 improves from 0.334 to 0.427. CITATION remains the largest and most important entity type, while ORG remains difficult because the current annotated dataset contains relatively few ORG examples and the model does not yet learn reliable ORG patterns.
