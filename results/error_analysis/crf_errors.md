# CRF Error Analysis

## Error Category Counts

| Error Category | Count |
|---|---:|
| False negative | 99 |
| Boundary error | 10 |
| Type error | 7 |
| False positive | 6 |

## Error Counts by Entity Type

| Error Category | Entity Type | Count |
|---|---|---:|
| False negative | PARTY | 68 |
| False negative | ORG | 14 |
| False negative | CITATION | 12 |
| Type error | CITATION | 5 |
| Boundary error | PARTY | 5 |
| Boundary error | CITATION | 5 |
| False negative | DATE | 4 |
| False positive | CITATION | 3 |
| False positive | STATUTE | 2 |
| Type error | COURT | 1 |
| Type error | PARTY | 1 |
| False positive | PARTY | 1 |
| False negative | JUDGE | 1 |

## Representative Error Examples

### Example 1: Type error (CITATION)

- Gold: `1055 Allen`
- Predicted: `510 U . S . 1055 Allen v . Gallagher . No . 93 - 6691`
- Context: # # # SAMPLE 76 510 U . S . 1055 Allen v . Gallagher . No . 93 - 6691 . Supreme Court of United States . January

### Example 2: Boundary error (PARTY)

- Gold: `Motions of petitioners for leave to proceed in forma pauperis granted . Certiorari granted , judgments vacated , and cases remanded for further consideration in light of United States`
- Predicted: `United States`
- Context: cases remanded for further consideration in light of United States v . Booker , ante , p .

### Example 3: Type error (COURT)

- Gold: `The petition for a writ of certiorari is granted and the judgment is vacated . The case is remanded to the Court of Appeals for further consideration in light of United States`
- Predicted: `Court of Appeals`
- Context: vacated . The case is remanded to the Court of Appeals for further consideration in light of United States

### Example 4: Boundary error (PARTY)

- Gold: `The petition for a writ of certiorari is granted and the judgment is vacated . The case is remanded to the Court of Appeals for further consideration in light of United States`
- Predicted: `United States`
- Context: of Appeals for further consideration in light of United States v . Donruss Co . , ante ,

### Example 5: Type error (CITATION)

- Gold: `1128 LACY`
- Predicted: `537 U . S . 1128 LACY v . MISSISSIPPI . No . 02 - 7395`
- Context: # # # SAMPLE 63 537 U . S . 1128 LACY v . MISSISSIPPI . No . 02 - 7395 . Supreme Court of United States . January

### Example 6: Boundary error (CITATION)

- Gold: `59 U . S . 584 ( 1855 )`
- Predicted: `59 U`
- Context: # # # SAMPLE 68 59 U . S . 584 ( 1855 ) 18

### Example 7: Boundary error (PARTY)

- Gold: `Hazeltine`
- Predicted: `Hazeltine Research , Inc`
- Context: Automatic Radio Mfg . Co . v . Hazeltine Research , Inc . , 339 U . S . 827

### Example 8: Boundary error (CITATION)

- Gold: `138 U . S . 252 , 255 ( 1891 )`
- Predicted: `Waterman v . Mackenzie , 138 U`
- Context: . See , e . g . , Waterman v . Mackenzie , 138 U . S . 252 , 255 ( 1891

### Example 9: Boundary error (PARTY)

- Gold: `United States`
- Predicted: `United States , 332 U`
- Context: ) ; International Salt Co . v . United States , 332 U . S . 392 , 395 - 396

### Example 10: Boundary error (CITATION)

- Gold: `379 U . S . 29 , 33 ( 1964 )`
- Predicted: `379 U . S . 29`
- Context: " Brulotte v . Thys Co . , 379 U . S . 29 , 33 ( 1964 ) . And just

### Example 11: Type error (CITATION)

- Gold: `Brulotte`
- Predicted: `Brulotte v . Thys Co`
- Context: of the patent ' s teachings . In Brulotte v . Thys Co . , supra , the patentee licensed the

### Example 12: Boundary error (PARTY)

- Gold: `Hazeltine`
- Predicted: `Hazeltine Research , Inc`
- Context: Automatic Radio Mfg . Co . v . Hazeltine Research , Inc . , 339 U . S . 827

### Example 13: Type error (PARTY)

- Gold: `Hansberry v . Lee , 311 U`
- Predicted: `Hansberry`
- Context: made a party by service of process . Hansberry v . Lee , 311 U . S

### Example 14: Boundary error (CITATION)

- Gold: `Hansberry v . Lee , 311 U`
- Predicted: `311 U . S . 32 , 40 - 41 ( 1940 )`
- Context: of process . Hansberry v . Lee , 311 U . S . 32 , 40 - 41 ( 1940 ) . The consistent constitutional rule has been that

### Example 15: Type error (CITATION)

- Gold: `Pennoyer`
- Predicted: `Pennoyer v . Neff , 95 U . S . 714 ( 1878 )`
- Context: the defendant . E . g . , Pennoyer v . Neff , 95 U . S . 714 ( 1878 ) ; Vanderbilt v . Vanderbilt , 354 U

### Example 16: Boundary error (CITATION)

- Gold: `Vanderbilt v . Vanderbilt , 354 U . S . 416 , 418`
- Predicted: `Vanderbilt v . Vanderbilt , 354 U . S . 416 , 418 ( 1957 )`
- Context: . S . 714 ( 1878 ) ; Vanderbilt v . Vanderbilt , 354 U . S . 416 , 418 ( 1957 ) . Here , Hazeltine was not named as

### Example 17: Type error (CITATION)

- Gold: `Fed . Rule Civ . Proc . 65 ( d )`
- Predicted: `Rule Civ . Proc . 65 ( d )`
- Context: personal service or otherwise , " Fed . Rule Civ . Proc . 65 ( d ) , a nonparty with notice cannot be held

### Example 18: False positive (STATUTE)

- Gold: `O`
- Predicted: `Act of 1917`
- Context: very considerable discretion upon the Secretary . The Act of 1917 , however , drops the language of discretion

### Example 19: False positive (STATUTE)

- Gold: `O`
- Predicted: `Act of 1917`
- Context: enter into possession . To assume that the Act of 1917 , while directing the Secretary to make allotments

### Example 20: False positive (CITATION)

- Gold: `O`
- Predicted: `Bement v . National Harrow Co`
- Context: . See , e . g . , Bement v . National Harrow Co . , 186 U . S . 70

### Example 21: False positive (PARTY)

- Gold: `O`
- Predicted: `Eastern Paper Bag Co`
- Context: , Continental Paper Bag Co . v . Eastern Paper Bag Co . , 210 U . S . 405

### Example 22: False positive (CITATION)

- Gold: `O`
- Predicted: `Laitram Corp . v . King Crab , Inc`
- Context: . 637 , 641 ( 1947 ) ; Laitram Corp . v . King Crab , Inc . , 245 F . Supp . 1019

### Example 23: False positive (CITATION)

- Gold: `O`
- Predicted: `239 F`
- Context: handed down on January 25 , 1965 , 239 F . Supp . , at 76 , the

### Example 24: False negative (PARTY)

- Gold: `854 NOVAK`
- Predicted: `O`
- Context: # SAMPLE 13 537 U . S . 854 NOVAK v . UNITED STATES . No . 01

### Example 25: False negative (PARTY)

- Gold: `Gallagher`
- Predicted: `O`
- Context: U . S . 1055 Allen v . Gallagher . No . 93 - 6691 . Supreme

### Example 26: False negative (CITATION)

- Gold: `No . 93 - 6691`
- Predicted: `O`
- Context: S . 1055 Allen v . Gallagher . No . 93 - 6691 . Supreme Court of United States . January

### Example 27: False negative (CITATION)

- Gold: `C . A . 11th Cir`
- Predicted: `O`
- Context: OF APPEALS FOR THE ELEVENTH CIRCUIT . 22 C . A . 11th Cir . Certiorari denied . Reported below : 45

### Example 28: False negative (CITATION)

- Gold: `45 Fed . Appx . 884`
- Predicted: `O`
- Context: Cir . Certiorari denied . Reported below : 45 Fed . Appx . 884 .

### Example 29: False negative (CITATION)

- Gold: `C . A . 11th Cir`
- Predicted: `O`
- Context: # # # SAMPLE 95 11 C . A . 11th Cir . Reported below : 112 Fed . Appx

### Example 30: False negative (CITATION)

- Gold: `112 Fed . Appx . 4`
- Predicted: `O`
- Context: A . 11th Cir . Reported below : 112 Fed . Appx . 4 ; Motions of petitioners for leave to proceed

### Example 31: False negative (PARTY)

- Gold: `Booker , ante , p`
- Predicted: `O`
- Context: consideration in light of United States v . Booker , ante , p . 220 .

### Example 32: False negative (PARTY)

- Gold: `1173 CANEDO GARCIA`
- Predicted: `O`
- Context: # SAMPLE 104 537 U . S . 1173 CANEDO GARCIA v . CASTRO , WARDEN . No .

### Example 33: False negative (PARTY)

- Gold: `CASTRO , WARDEN`
- Predicted: `O`
- Context: . S . 1173 CANEDO GARCIA v . CASTRO , WARDEN . No . 02 - 7602 . Supreme

### Example 34: False negative (CITATION)

- Gold: `393 U . S . 478 ( 1969 )`
- Predicted: `O`
- Context: # # # SAMPLE 38 393 U . S . 478 ( 1969 ) COMMISSIONER OF INTERNAL REVENUE v . SHAW -

### Example 35: False negative (PARTY)

- Gold: `Donruss Co`
- Predicted: `O`
- Context: consideration in light of United States v . Donruss Co . , ante , p . 297 .

### Example 36: False negative (PARTY)

- Gold: `MISSISSIPPI`
- Predicted: `O`
- Context: U . S . 1128 LACY v . MISSISSIPPI . No . 02 - 7395 . Supreme

### Example 37: False negative (CITATION)

- Gold: `No . 02 - 7395`
- Predicted: `O`
- Context: S . 1128 LACY v . MISSISSIPPI . No . 02 - 7395 . Supreme Court of United States . January

### Example 38: False negative (CITATION)

- Gold: `821 So . 2d 850`
- Predicted: `O`
- Context: Miss . Certiorari denied . Reported below : 821 So . 2d 850 .

### Example 39: False negative (CITATION)

- Gold: `18 How . 584`
- Predicted: `O`
- Context: U . S . 584 ( 1855 ) 18 How . 584 WILLIAM B . CULBERTSON , APPELLANT , v

### Example 40: False negative (PARTY)

- Gold: `HRI`
- Predicted: `O`
- Context: affirmed by the Court of Appeals , and HRI has not challenged that award in this Court

### Example 41: False negative (PARTY)

- Gold: `HRI`
- Predicted: `O`
- Context: Paragraph A of the injunction , which enjoined HRI from " A . Conditioning directly or indirectly

### Example 42: False negative (PARTY)

- Gold: `Zenith`
- Predicted: `O`
- Context: of a license to defendant - counterclaimant , Zenith Radio Corporation , or any of its subsidiaries

### Example 43: False negative (PARTY)

- Gold: `HRI`
- Predicted: `O`
- Context: This paragraph of the injunction was directed at HRI ' s policy of insisting upon acceptance of

### Example 44: False negative (PARTY)

- Gold: `Zenith`
- Predicted: `O`
- Context: 16 of the Clayton Act , under which Zenith had sought and the District Court had granted

### Example 45: False negative (PARTY)

- Gold: `HRI`
- Predicted: `O`
- Context: television sets , irrespective of the use of HRI ' s inventions . The injunction reaches only

### Example 46: False negative (CITATION)

- Gold: `332 U . S . 392 , 395 - 396 ( 1947 )`
- Predicted: `O`
- Context: Salt Co . v . United States , 332 U . S . 392 , 395 - 396 ( 1947 ) . His right to set the price for

### Example 47: False negative (PARTY)

- Gold: `Thys Co`
- Predicted: `O`
- Context: ' s teachings . In Brulotte v . Thys Co . , supra , the patentee licensed the

### Example 48: False negative (PARTY)

- Gold: `HRI`
- Predicted: `O`
- Context: the privilege of using all present and future HRI patents by promising to pay a percentage royalty

### Example 49: False negative (PARTY)

- Gold: `HRI`
- Predicted: `O`
- Context: of $ 10 , 000 per year . HRI sued for the minimum royalty and other sums

### Example 50: False negative (PARTY)

- Gold: `HRI`
- Predicted: `O`
- Context: avoid determining whether each radio receiver embodied an HRI patent . The percentage royalty was deemed an

### Example 51: False negative (PARTY)

- Gold: `HRI`
- Predicted: `O`
- Context: formula at issue and did not indicate that HRI used its patent leverage to coerce a promise

### Example 52: False negative (PARTY)

- Gold: `HRI`
- Predicted: `O`
- Context: . Whether the trial court correctly determined that HRI was conditioning the grant of patent licenses upon

### Example 53: False negative (PARTY)

- Gold: `Zenith`
- Predicted: `O`
- Context: 2 of the Sherman Act , or that Zenith was threatened by a violation so as to

### Example 54: False negative (CITATION)

- Gold: `245 F . Supp . 1019 ( D . C . Alaska 1965 )`
- Predicted: `O`
- Context: v . King Crab , Inc . , 245 F . Supp . 1019 ( D . C . Alaska 1965 ) . See also Report of the Attorney General

### Example 55: False negative (PARTY)

- Gold: `Hazeltine`
- Predicted: `O`
- Context: be denied that the Court there sustained a Hazeltine patent license of precisely the same tenor as

### Example 56: False negative (PARTY)

- Gold: `Hazeltine`
- Predicted: `O`
- Context: Radio Court did not consider it relevant whether Hazeltine Research had " insisted " upon inclusion of

### Example 57: False negative (PARTY)

- Gold: `Zenith`
- Predicted: `O`
- Context: at 76 , the District Court concluded that Zenith had suffered actual damages of $ 16 ,

### Example 58: False negative (PARTY)

- Gold: `Zenith`
- Predicted: `O`
- Context: the restraints imposed by the three pools upon Zenith ' s export business during the four -

### Example 59: False negative (PARTY)

- Gold: `HAZELTINE`
- Predicted: `O`
- Context: # SAMPLE 8 I . THE JUDGMENTS AGAINST HAZELTINE . The named plaintiff in the patent infringement

### Example 60: False negative (PARTY)

- Gold: `HRI`
- Predicted: `O`
- Context: patent infringement complaint which began this litigation was HRI , not its parent , Hazeltine ; Zenith

### Example 61: False negative (PARTY)

- Gold: `Hazeltine`
- Predicted: `O`
- Context: litigation was HRI , not its parent , Hazeltine ; Zenith ' s counterclaim named only HRI

### Example 62: False negative (PARTY)

- Gold: `Zenith`
- Predicted: `O`
- Context: HRI , not its parent , Hazeltine ; Zenith ' s counterclaim named only HRI as the

### Example 63: False negative (PARTY)

- Gold: `HRI`
- Predicted: `O`
- Context: Hazeltine ; Zenith ' s counterclaim named only HRI as the " counter - defendant , "

### Example 64: False negative (PARTY)

- Gold: `HRI`
- Predicted: `O`
- Context: the " counter - defendant , " identifying HRI and Hazeltine as " counter - defendant and

### Example 65: False negative (PARTY)

- Gold: `Hazeltine`
- Predicted: `O`
- Context: counter - defendant , " identifying HRI and Hazeltine as " counter - defendant and its parent

### Example 66: False negative (PARTY)

- Gold: `Zenith`
- Predicted: `O`
- Context: - defendant and its parent . " After Zenith had filed its answer and had delivered a

### Example 67: False negative (PARTY)

- Gold: `HRI`
- Predicted: `O`
- Context: a draft of its counter - claim to HRI ' s attorneys - b the answer and

### Example 68: False negative (PARTY)

- Gold: `HRI`
- Predicted: `O`
- Context: b the answer and the counterclaim alleging that HRI had unlawfully conspired with Hazeltine and foreign patent

### Example 69: False negative (PARTY)

- Gold: `Hazeltine`
- Predicted: `O`
- Context: counterclaim alleging that HRI had unlawfully conspired with Hazeltine and foreign patent pools - H and Zenith

### Example 70: False negative (PARTY)

- Gold: `Zenith`
- Predicted: `O`
- Context: Hazeltine and foreign patent pools - H and Zenith stipulated that " for purpose of this litigation

### Example 71: False negative (PARTY)

- Gold: `Hazeltine`
- Predicted: `O`
- Context: purpose of this litigation Plaintiff and its parent Hazeltine Corporation will be considered to be one and

### Example 72: False negative (PARTY)

- Gold: `Zenith`
- Predicted: `O`
- Context: weeks after the stipulation had been signed , Zenith filed its counterclaim , seeking money damages from

### Example 73: False negative (ORG)

- Gold: `HRI`
- Predicted: `O`
- Context: filed its counterclaim , seeking money damages from HRI and an injunction against HRI and those "

### Example 74: False negative (ORG)

- Gold: `HRI`
- Predicted: `O`
- Context: money damages from HRI and an injunction against HRI and those " in privity " with it

### Example 75: False negative (PARTY)

- Gold: `Hazeltine`
- Predicted: `O`
- Context: those " in privity " with it . Hazeltine was not served with the counterclaim and was

### Example 76: False negative (ORG)

- Gold: `HRI`
- Predicted: `O`
- Context: it was alleged to be a coconspirator with HRI and the foreign patent pools . Hazeltine made

### Example 77: False negative (PARTY)

- Gold: `Hazeltine`
- Predicted: `O`
- Context: with HRI and the foreign patent pools . Hazeltine made no appearance in the litigation until Zenith

### Example 78: False negative (PARTY)

- Gold: `Zenith`
- Predicted: `O`
- Context: Hazeltine made no appearance in the litigation until Zenith proposed that judgment be entered against it ,

### Example 79: False negative (PARTY)

- Gold: `Hazeltine`
- Predicted: `O`
- Context: be entered against it , at which time Hazeltine filed a " special appearance . " Insofar

### Example 80: False negative (PARTY)

- Gold: `Hazeltine`
- Predicted: `O`
- Context: . " Insofar as the record reveals , Hazeltine did not formally participate in the proceedings until
