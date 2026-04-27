# Error Analysis for CRF Test Predictions

## Error counts
- False negative: 466
- False positive: 17
- Wrong type: 12
- BIO boundary error: 10

## Error counts by entity type

### CITATION
- False negative: 405
- False positive: 11
- BIO boundary error: 9

### COURT
- False negative: 19
- False positive: 5

### DATE
- False negative: 23
- Wrong type: 7
- False positive: 1
- BIO boundary error: 1

### ORG
- False negative: 19
- Wrong type: 5

## Representative examples

### CITATION — BIO boundary error
- Token: `Act` | Gold: `B-CITATION` | Pred: `I-CITATION`
  - Context: statute of Michigan enacted in 1923 ( [Act] No . 233 , Public Acts 1923
- Token: `Act` | Gold: `B-CITATION` | Pred: `I-CITATION`
  - Context: the statute in 1927 and 1929 ( [Act] No . 140 , Public Acts 1927
- Token: `Trust` | Gold: `I-CITATION` | Pred: `B-CITATION`
  - Context: a business conducted by receivers . Central [Trust] Co . v . N . Y
- Token: `18` | Gold: `I-CITATION` | Pred: `B-CITATION`
  - Context: 768 ; People v . Hopkins , [18] F . ( 2d ) 731 .
- Token: `Murray` | Gold: `I-CITATION` | Pred: `B-CITATION`
  - Context: 129 N . E . 886 ; [Murray] v . Chicago & N . W

### CITATION — False negative
- Token: `541` | Gold: `B-CITATION` | Pred: `O`
  - Context: [541] U . S . 929 OZMINT ,
- Token: `U` | Gold: `I-CITATION` | Pred: `O`
  - Context: 541 [U] . S . 929 OZMINT , DIRECTOR
- Token: `.` | Gold: `I-CITATION` | Pred: `O`
  - Context: 541 U [.] S . 929 OZMINT , DIRECTOR ,
- Token: `S` | Gold: `I-CITATION` | Pred: `O`
  - Context: 541 U . [S] . 929 OZMINT , DIRECTOR , SOUTH
- Token: `.` | Gold: `I-CITATION` | Pred: `O`
  - Context: 541 U . S [.] 929 OZMINT , DIRECTOR , SOUTH CAROLINA

### CITATION — False positive
- Token: `.` | Gold: `O` | Pred: `I-CITATION`
  - Context: 7416 . Supreme Court of United States [.] January 24 , 2005 . Mr
- Token: `.` | Gold: `O` | Pred: `I-CITATION`
  - Context: United States . January 24 , 2005 [.] Mr Coxe , for plaintiff ;
- Token: `(` | Gold: `O` | Pred: `I-CITATION`
  - Context: a statute of Michigan enacted in 1923 [(] Act No . 233 , Public Acts
- Token: `)` | Gold: `O` | Pred: `I-CITATION`
  - Context: , Public Acts 1923 , § 4 [)] , " every corporation organized or doing
- Token: `and` | Gold: `O` | Pred: `I-CITATION`
  - Context: were amendments of the statute in 1927 [and] 1929 ( Act No . 140 ,

### COURT — False negative
- Token: `Supreme` | Gold: `B-COURT` | Pred: `O`
  - Context: , RECEIVER . No . 598 . [Supreme] Court of United States . Argued April
- Token: `Court` | Gold: `I-COURT` | Pred: `O`
  - Context: RECEIVER . No . 598 . Supreme [Court] of United States . Argued April 19
- Token: `of` | Gold: `I-COURT` | Pred: `O`
  - Context: . No . 598 . Supreme Court [of] United States . Argued April 19 ,
- Token: `United` | Gold: `I-COURT` | Pred: `O`
  - Context: No . 598 . Supreme Court of [United] States . Argued April 19 , 1932
- Token: `States` | Gold: `I-COURT` | Pred: `O`
  - Context: . 598 . Supreme Court of United [States] . Argued April 19 , 1932 .

### COURT — False positive
- Token: `Supreme` | Gold: `O` | Pred: `B-COURT`
  - Context: . No . 04 - 7416 . [Supreme] Court of United States . January 24
- Token: `Court` | Gold: `O` | Pred: `I-COURT`
  - Context: No . 04 - 7416 . Supreme [Court] of United States . January 24 ,
- Token: `of` | Gold: `O` | Pred: `I-COURT`
  - Context: . 04 - 7416 . Supreme Court [of] United States . January 24 , 2005
- Token: `United` | Gold: `O` | Pred: `I-COURT`
  - Context: 04 - 7416 . Supreme Court of [United] States . January 24 , 2005 .
- Token: `States` | Gold: `O` | Pred: `I-COURT`
  - Context: - 7416 . Supreme Court of United [States] . January 24 , 2005 .

### DATE — BIO boundary error
- Token: `1929` | Gold: `B-DATE` | Pred: `I-DATE`
  - Context: to do this till December 30 , [1929] , when the court made an order

### DATE — False negative
- Token: `March` | Gold: `B-DATE` | Pred: `O`
  - Context: . Supreme Court of United States . [March] 19 , 2004 . 543 U
- Token: `19` | Gold: `I-DATE` | Pred: `O`
  - Context: Supreme Court of United States . March [19] , 2004 . 543 U .
- Token: `,` | Gold: `I-DATE` | Pred: `O`
  - Context: Court of United States . March 19 [,] 2004 . 543 U . S
- Token: `2004` | Gold: `I-DATE` | Pred: `O`
  - Context: of United States . March 19 , [2004] . 543 U . S .
- Token: `.` | Gold: `I-DATE` | Pred: `O`
  - Context: United States . March 19 , 2004 [.] 543 U . S . 1127

### DATE — False positive
- Token: `,` | Gold: `O` | Pred: `I-DATE`
  - Context: continued to do this till December 30 [,] 1929 , when the court made an

### DATE — Wrong type
- Token: `January` | Gold: `B-DATE` | Pred: `I-CITATION`
  - Context: . Supreme Court of United States . [January] 24 , 2005 . Mr Coxe
- Token: `24` | Gold: `I-DATE` | Pred: `I-CITATION`
  - Context: Supreme Court of United States . January [24] , 2005 . Mr Coxe ,
- Token: `,` | Gold: `I-DATE` | Pred: `I-CITATION`
  - Context: Court of United States . January 24 [,] 2005 . Mr Coxe , for
- Token: `2005` | Gold: `I-DATE` | Pred: `I-CITATION`
  - Context: of United States . January 24 , [2005] . Mr Coxe , for plaintiff
- Token: `1927` | Gold: `B-DATE` | Pred: `B-CITATION`
  - Context: There were amendments of the statute in [1927] and 1929 ( Act No . 140

### ORG — False negative
- Token: `State` | Gold: `B-ORG` | Pred: `O`
  - Context: A petition by the People of the [State] of Michigan that a receiver appointed by
- Token: `of` | Gold: `I-ORG` | Pred: `O`
  - Context: petition by the People of the State [of] Michigan that a receiver appointed by a
- Token: `Michigan` | Gold: `I-ORG` | Pred: `O`
  - Context: by the People of the State of [Michigan] that a receiver appointed by a federal
- Token: `Hammond` | Gold: `B-ORG` | Pred: `O`
  - Context: ( In re G . H . [Hammond] Co . , 246 Mich . 179
- Token: `Co` | Gold: `I-ORG` | Pred: `O`
  - Context: In re G . H . Hammond [Co] . , 246 Mich . 179 ;

### ORG — Wrong type
- Token: `Kingsport` | Gold: `B-ORG` | Pred: `I-CITATION`
  - Context: , 52 , 54 ; cf . [Kingsport] Press v . Brief English Systems ,
- Token: `Press` | Gold: `I-ORG` | Pred: `I-CITATION`
  - Context: 52 , 54 ; cf . Kingsport [Press] v . Brief English Systems , 54
- Token: `Brief` | Gold: `B-ORG` | Pred: `I-CITATION`
  - Context: ; cf . Kingsport Press v . [Brief] English Systems , 54 F . (
- Token: `English` | Gold: `I-ORG` | Pred: `I-CITATION`
  - Context: cf . Kingsport Press v . Brief [English] Systems , 54 F . ( 2d
- Token: `Systems` | Gold: `I-ORG` | Pred: `I-CITATION`
  - Context: . Kingsport Press v . Brief English [Systems] , 54 F . ( 2d )

## Interpretation
The dominant error type is false negatives, meaning the CRF often leaves gold entities unlabeled. This is consistent with the small annotated dataset and the skew toward CITATION entities. ORG remains especially difficult because it appears less frequently and has more variable surface forms. Some errors are BIO boundary errors, especially around legal citations split by punctuation or reporter abbreviations. The paragraph-similarity analysis also suggests that citation fragments sometimes span adjacent text chunks, which can hurt recall.
