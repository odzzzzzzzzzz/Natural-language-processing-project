# Annotation Provenance and Reliability Note

## Annotation Provenance

The project contains two manually annotated annotation sets.

| Annotation Set | Size | Annotator | Purpose |
|---|---:|---|---|
| Pilot sample set | 50 passages | Yulong Ou | Initial annotation pilot, guideline testing, and early pipeline development |
| Expanded corpus | 150 passages | Guyu Sun | Main experimental corpus used for train/dev/test splitting and model evaluation |

The 50-passage pilot set and the 150-passage expanded corpus do not overlap. Therefore, these files show that more than one team member contributed to annotation, but they do not constitute a valid inter-annotator agreement setup.

## Why We Do Not Report IAA

Inter-annotator agreement requires at least two annotators to independently label the same passages. Since the Yulong and Guyu annotation sets cover different passages, we do not report Cohen's kappa or pairwise span-level F1 as IAA metrics.

## Paper-Ready Paragraph

The annotation work was divided across team members. Yulong Ou annotated an initial 50-passage pilot set, which was used to test the annotation schema, BIO conversion, and early preprocessing pipeline. Guyu Sun annotated the expanded 150-passage corpus, which serves as the main experimental dataset for model training, development, and testing. Because the two annotation sets do not overlap, we treat them as separate annotation phases rather than as an inter-annotator agreement study. As a result, we do not report Cohen's kappa or pairwise annotator F1 in the current pilot version. Future work should include a shared overlapping subset annotated independently by multiple annotators, followed by adjudication.

## Presentation Version

For annotation, we first created a 50-passage pilot set annotated by Yulong to test the schema and pipeline. Then we expanded to a 150-passage corpus annotated by Guyu, which became the main dataset for experiments. Since these two sets did not overlap, we cannot honestly report IAA yet, but we can clearly report the annotation provenance and discuss IAA as future work.
