# Error Analysis: CRF_Tuned

## Span-Level Confusion Summary

| Model | TP | FP | FN |
|---|---:|---:|---:|
| CRF_Tuned | 88 | 19 | 108 |

## Error Category Counts

| Error Category | Count |
|---|---:|
| False negative | 96 |
| False positive | 7 |
| Boundary error | 6 |
| Type error | 6 |

## Error Counts by Entity Type

| Error Category | Entity Type | Count |
|---|---|---:|
| False negative | PARTY | 69 |
| False negative | ORG | 14 |
| False negative | CITATION | 8 |
| False negative | DATE | 5 |
| False positive | CITATION | 5 |
| Boundary error | PARTY | 4 |
| Type error | PARTY | 3 |
| Type error | CITATION | 2 |
| Boundary error | CITATION | 2 |
| Type error | STATUTE | 1 |
| False positive | COURT | 1 |
| False positive | PARTY | 1 |

## Representative Error Examples

### Example 1: Boundary error (PARTY)

- Gold: `Motions of petitioners for leave to proceed in forma pauperis granted . Certiorari granted , judgments vacated , and cases remanded for further consideration in light of United States`
- Predicted: `United States`
- Context: Cir . Reported below : 112 Fed . Appx . 4 ; Motions of petitioners for leave to proceed in forma pauperis granted . Certiorari granted , judgments vacated , and cases remanded for further consideration in light of United States v . Booker , ante , p . 220 .

### Example 2: Boundary error (PARTY)

- Gold: `The petition for a writ of certiorari is granted and the judgment is vacated . The case is remanded to the Court of Appeals for further consideration in light of United States`
- Predicted: `United States`
- Context: . Carroll , Jr . , for respondent . PER CURIAM . The petition for a writ of certiorari is granted and the judgment is vacated . The case is remanded to the Court of Appeals for further consideration in light of United States v . Donruss Co . , ante , p . 297 .

### Example 3: Type error (PARTY)

- Gold: `1128 LACY`
- Predicted: `537 U . S . 1128 LACY v . MISSISSIPPI . No . 02 - 7395`
- Context: # # # SAMPLE 63 537 U . S . 1128 LACY v . MISSISSIPPI . No . 02 - 7395 . Supreme Court

### Example 4: Boundary error (PARTY)

- Gold: `Hazeltine`
- Predicted: `Hazeltine Research , Inc`
- Context: under its view of Automatic Radio Mfg . Co . v . Hazeltine Research , Inc . , 339 U . S . 827 (

### Example 5: Type error (CITATION)

- Gold: `261 U . S . 24 ( 1923 )`
- Predicted: `Nye Tool & Machine Works , 261 U`
- Context: & Tool Co . v . Nye Tool & Machine Works , 261 U . S . 24 ( 1923 ) . The law also recognizes that he may assign to another his

### Example 6: Boundary error (CITATION)

- Gold: `138 U . S . 252 , 255 ( 1891 )`
- Predicted: `Waterman v . Mackenzie , 138 U . S . 252 , 255`
- Context: See , e . g . , Waterman v . Mackenzie , 138 U . S . 252 , 255 ( 1891 ) . But there are established limits which the patentee must not exceed

### Example 7: Type error (PARTY)

- Gold: `Brulotte`
- Predicted: `Brulotte v . Thys Co`
- Context: not attributable to use of the patent ' s teachings . In Brulotte v . Thys Co . , supra , the patentee licensed the

### Example 8: Boundary error (PARTY)

- Gold: `Hazeltine`
- Predicted: `Hazeltine Research , Inc`
- Context: of this Court , Automatic Radio Mfg . Co . v . Hazeltine Research , Inc . , 339 U . S . 827 (

### Example 9: Type error (CITATION)

- Gold: `Hansberry v . Lee , 311 U`
- Predicted: `Lee , 311 U`
- Context: he has not been made a party by service of process . Hansberry v . Lee , 311 U . S . 32 , 40 - 41 ( 1940 ) .

### Example 10: Type error (PARTY)

- Gold: `Pennoyer`
- Predicted: `Pennoyer v . Neff , 95 U`
- Context: over the person of the defendant . E . g . , Pennoyer v . Neff , 95 U . S . 714 ( 1878

### Example 11: Boundary error (CITATION)

- Gold: `Vanderbilt v . Vanderbilt , 354 U . S . 416 , 418`
- Predicted: `Vanderbilt v . Vanderbilt , 354 U . S . 416 , 418 ( 1957 )`
- Context: Neff , 95 U . S . 714 ( 1878 ) ; Vanderbilt v . Vanderbilt , 354 U . S . 416 , 418 ( 1957 ) . Here , Hazeltine was not named as a

### Example 12: Type error (STATUTE)

- Gold: `Fed . Rule Civ . Proc . 65 ( d )`
- Predicted: `Rule Civ . Proc . 65 ( d )`
- Context: actual notice of the order by personal service or otherwise , " Fed . Rule Civ . Proc . 65 ( d ) , a nonparty with notice cannot be held in contempt until shown

### Example 13: False negative (PARTY)

- Gold: `854 NOVAK`
- Context: # # # SAMPLE 13 537 U . S . 854 NOVAK v . UNITED STATES . No . 01 - 10642 . Supreme

### Example 14: False negative (PARTY)

- Gold: `1055 Allen`
- Context: # # # SAMPLE 76 510 U . S . 1055 Allen v . Gallagher . No . 93 - 6691 . Supreme Court

### Example 15: False negative (PARTY)

- Gold: `Gallagher`
- Context: # SAMPLE 76 510 U . S . 1055 Allen v . Gallagher . No . 93 - 6691 . Supreme Court of United States

### Example 16: False negative (CITATION)

- Gold: `C . A . 11th Cir`
- Context: THE UNITED STATES COURT OF APPEALS FOR THE ELEVENTH CIRCUIT . 22 C . A . 11th Cir . Certiorari denied . Reported below : 45 Fed . Appx .

### Example 17: False negative (CITATION)

- Gold: `45 Fed . Appx . 884`
- Context: . A . 11th Cir . Certiorari denied . Reported below : 45 Fed . Appx . 884 .

### Example 18: False negative (CITATION)

- Gold: `C . A . 11th Cir`
- Context: # # # SAMPLE 95 11 C . A . 11th Cir . Reported below : 112 Fed . Appx . 4 ; Motions

### Example 19: False negative (PARTY)

- Gold: `Booker , ante , p`
- Context: cases remanded for further consideration in light of United States v . Booker , ante , p . 220 .

### Example 20: False negative (PARTY)

- Gold: `1173 CANEDO GARCIA`
- Context: # # # SAMPLE 104 537 U . S . 1173 CANEDO GARCIA v . CASTRO , WARDEN . No . 02 - 7602 .
