# Stage 4 Post-processing Ablation Summary

Baseline CRF span-level result: Precision = 0.781, Recall = 0.418, F1 = 0.545.

| System | Precision | Recall | F1 | TP | FP | FN | Main Tag Changes |
|---|---:|---:|---:|---:|---:|---:|---:|
| CRF baseline | 0.781 | 0.418 | 0.545 | 82 | 23 | 114 | 0 |
| CRF_Post_BIOOnly | 0.781 | 0.418 | 0.545 | 82 | 23 | 114 | 0 |
| CRF_Post_SpanCompletionOnly | 0.621 | 0.327 | 0.428 | 64 | 39 | 132 | 84 |
| CRF_Post_NestedOnly | 0.781 | 0.418 | 0.545 | 82 | 23 | 114 | 0 |
| CRF_Post_TypeConsistencyOnly | 0.781 | 0.418 | 0.545 | 82 | 23 | 114 | 0 |

## Interpretation Template

Use this table to identify which Stage 4 component changes performance.
If span-completion-only lowers F1 substantially, then the full post-processing degradation is mainly caused by over-expanding entity boundaries.
If type-consistency-only changes little, then repeated-string voting is not a major source of either improvement or harm in this test set.
If nested-only changes little, then the current CRF predictions rarely contain overlapping spans that need resolution.
