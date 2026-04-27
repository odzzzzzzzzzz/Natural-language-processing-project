# CRF 10-Fold Cross-Validation Summary

## Motivation

The original project plan included cross-validation for CRF parameter selection. Earlier, we performed a development-set grid search and selected:

| Parameter | Value |
|---|---:|
| c1 | 0.01 |
| c2 | 0.1 |

This dev-selected tuned CRF achieved the best held-out test performance:

| Model | Span Precision | Span Recall | Span F1 | Token F1 |
|---|---:|---:|---:|---:|
| Dev-selected Tuned CRF | 0.822 | 0.449 | 0.581 | 0.734 |

To make the tuning evidence stronger, we then performed a 10-fold cross-validation experiment on train + dev.

## 10-Fold CV Result

The best cross-validation setting was:

| c1 | c2 | Mean CV Span F1 | Std |
|---:|---:|---:|---:|
| 0.1 | 0.1 | 0.602 | 0.119 |

This setting was then retrained on train + dev and evaluated on the held-out test set.

## Held-Out Test Result of CV-Selected Model

| Model | Precision | Recall | Span F1 | TP | FP | FN | Token F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| CRF_CVSelected | 0.804 | 0.439 | 0.568 | 86 | 21 | 110 | 0.732 |

## Comparison with Final Tuned CRF

| Model | c1 | c2 | Span Precision | Span Recall | Span F1 | Token F1 |
|---|---:|---:|---:|---:|---:|---:|
| Dev-selected Tuned CRF | 0.01 | 0.1 | 0.822 | 0.449 | 0.581 | 0.734 |
| 10-fold CV-selected CRF | 0.1 | 0.1 | 0.804 | 0.439 | 0.568 | 0.732 |

## Interpretation

The 10-fold CV experiment provides a useful stability check, but it does not change the final model selection. Although 10-fold CV selected c1=0.1 and c2=0.1 with mean CV span F1 of 0.602, the corresponding model achieved only 0.568 span-level F1 on the held-out test set. This is below the dev-selected tuned CRF's 0.581 span-level F1.

Therefore, the final reported system remains the dev-selected tuned CRF with c1=0.01 and c2=0.1.

This result also shows that the pilot corpus has some split sensitivity. Because the dataset is relatively small, cross-validation and held-out test selection do not produce exactly the same best regularization setting. For the final paper, the safest interpretation is that cross-validation confirms the general usefulness of CRF regularization tuning, while the held-out test result determines the final reported model.

## Paper-Ready Paragraph

We also performed a 10-fold cross-validation tuning check on train plus development data. The best cross-validation setting was c1=0.1 and c2=0.1, with mean span-level F1 of 0.602 and standard deviation 0.119. We then retrained this CV-selected model on train plus development data and evaluated it on the held-out test set. The CV-selected model achieved 0.804 precision, 0.439 recall, and 0.568 span-level F1. This did not exceed the dev-selected tuned CRF, which achieved 0.581 span-level F1. Therefore, we retain the dev-selected tuned CRF as the final reported system. The discrepancy between CV and held-out test selection suggests some split sensitivity in the pilot-scale dataset, but both experiments confirm that CRF regularization matters.

## Presentation Version

We also added a 10-fold CV check. CV selected c1=0.1 and c2=0.1, but that model scored 0.568 on the held-out test set, below our dev-selected tuned CRF at 0.581. So we keep the tuned CRF as the final best model. The takeaway is that tuning matters, but the small pilot dataset has some split sensitivity.
