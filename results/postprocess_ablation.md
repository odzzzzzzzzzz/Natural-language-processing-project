# Stage 4 Post-processing Ablation

This experiment isolates the effect of each Stage 4 post-processing component on the CRF test predictions.

## CRF_Post_BIOOnly

### Operation Statistics

| Operation | Count |
|---|---:|
| bio_repairs | 0 |
| tag_changes_total | 0 |

### Overall Span-Level Result

| Model | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CRF_Post_BIOOnly | 0.781 | 0.418 | 0.545 | 82 | 23 | 114 |

## CRF_Post_SpanCompletionOnly

### Operation Statistics

| Operation | Count |
|---|---:|
| bio_repairs | 0 |
| span_completions | 34 |
| nested_overlap_resolutions | 2 |
| tag_changes_total | 84 |

### Overall Span-Level Result

| Model | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CRF_Post_SpanCompletionOnly | 0.621 | 0.327 | 0.428 | 64 | 39 | 132 |

## CRF_Post_NestedOnly

### Operation Statistics

| Operation | Count |
|---|---:|
| nested_overlap_resolutions | 0 |
| tag_changes_total | 0 |

### Overall Span-Level Result

| Model | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CRF_Post_NestedOnly | 0.781 | 0.418 | 0.545 | 82 | 23 | 114 |

## CRF_Post_TypeConsistencyOnly

### Operation Statistics

| Operation | Count |
|---|---:|
| type_consistency_mappings | 6 |
| type_consistency_changes | 0 |
| tag_changes_total | 0 |

### Overall Span-Level Result

| Model | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| CRF_Post_TypeConsistencyOnly | 0.781 | 0.418 | 0.545 | 82 | 23 | 114 |
