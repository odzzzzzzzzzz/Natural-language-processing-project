# Final Evaluation Run Summary

This file records the final span-level evaluation commands used for the Legal NER project.

## Systems Evaluated

1. Majority baseline
2. CoNLL-2003 CRF transfer baseline
3. Stanza pretrained NER baseline
4. Rule-based baseline
5. Original legal-domain CRF
6. Tuned legal-domain CRF
7. CRF + POS features
8. CRF + gazetteer features
9. CRF + chunk features
10. CRF without Stage 2 rule-output features
11. CRF + BIO repair
12. CRF + full heuristic post-processing

## Final Best System

The final best model is the tuned legal-domain CRF:

- Precision: 0.822
- Recall: 0.449
- Span-level F1: 0.581

## Notes

This script does not retrain models.
It only reruns final span-level evaluation on existing prediction files.

Main result files:

- results/main_results.md
- results/final_all_model_comparison.md
- results/span_eval_Majority.md
- results/span_eval_CoNLL2003_CRF.md
- results/span_eval_Stanza.md
- results/span_eval_RuleBased.md
- results/span_eval_CRF.md
- results/span_eval_CRF_Tuned.md
- results/span_eval_CRF_POS.md
- results/span_eval_CRF_Gazetteer.md
- results/span_eval_CRF_Chunk.md
- results/span_eval_CRF_NoStage2.md
- results/span_eval_CRF_BIO_Repair.md
- results/span_eval_CRF_FullPostprocess.md
