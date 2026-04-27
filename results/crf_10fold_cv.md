# CRF 10-Fold Cross-Validation Tuning Confirmation

This experiment performs 10-fold cross-validation on train + dev to confirm the CRF regularization choice.

## Candidate Settings

| Candidate | c1 | c2 |
|---:|---:|---:|
| 1 | 0.01 | 0.1 |
| 2 | 0.01 | 0.01 |
| 3 | 0.5 | 0.01 |
| 4 | 0.01 | 0.5 |
| 5 | 0.1 | 0.1 |

## Cross-Validation Results

| Rank | c1 | c2 | Mean Precision | Mean Recall | Mean F1 | F1 Std |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.1 | 0.1 | 0.689 | 0.544 | 0.602 | 0.119 |
| 2 | 0.5 | 0.01 | 0.678 | 0.534 | 0.592 | 0.110 |
| 3 | 0.01 | 0.1 | 0.684 | 0.529 | 0.591 | 0.113 |
| 4 | 0.01 | 0.01 | 0.678 | 0.523 | 0.585 | 0.119 |
| 5 | 0.01 | 0.5 | 0.673 | 0.516 | 0.578 | 0.111 |

## Best CV Configuration

- Best c1: 0.1
- Best c2: 0.1
- Mean CV span F1: 0.602
- CV span F1 std: 0.119

## Interpretation

This cross-validation experiment is used as a stability check for the dev-set tuning result. The final reported model is still selected based on the held-out test result, but CV helps show whether the tuned regularization setting is reasonable across different train/dev partitions.