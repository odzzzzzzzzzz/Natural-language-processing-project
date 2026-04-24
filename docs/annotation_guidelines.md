# Annotation Guidelines for Legal Named Entity Recognition

## 1. Entity Types

We annotate the following entity types in U.S. Supreme Court opinions:

- PARTY  
  Names of litigants or case participants  
  Example: *Auciello Iron Works, Inc.*

- JUDGE  
  Names of judges or justices, including titles  
  Example: *Justice Marshall*, *MR. JUSTICE BRENNAN*

- COURT  
  Names of courts  
  Example: *Supreme Court of the United States*

- STATUTE  
  Legal statutes or constitutional provisions  
  Example: *Fourth Amendment*

- CITATION  
  Legal case citations (reporter format)  
  Example: *390 U.S. 377 (1968)*

- ORG  
  Organizations, agencies, or institutional bodies  
  Example: *National Labor Relations Board*

- DATE  
  Explicit calendar dates  
  Example: *March 21, 2005*

---

## 2. Tagging Scheme

We use the BIO tagging scheme:

- B-XXX : beginning of an entity
- I-XXX : inside an entity
- O     : outside any entity

### Example

John      B-PARTY  
Smith     I-PARTY  
v.        O  
United    B-PARTY  
States    I-PARTY  

---

## 3. Annotation Rules

### 3.1 General Rules

1. Entities must be contiguous spans (no gaps)
2. Overlapping entities are not allowed
3. Prefer longer, semantically complete spans over partial spans
4. Maintain consistency across similar cases

---

### 3.2 Type-Specific Rules

#### PARTY
- Include full legal names when available
- Include suffixes such as *Inc.*, *Corp.*, etc.

#### JUDGE
- Always include titles (e.g., *Justice*, *Judge*)
- Include multi-word titles (e.g., *MR. JUSTICE MARSHALL*)

#### COURT
- Include full official court names
- Do not label generic mentions like “the court” unless clearly referring to a named court

#### STATUTE
- Include full statute names if present
- Label constitutional references (e.g., *Fourth Amendment*)

#### CITATION
- Label the entire citation as one entity
- Include volume, reporter, and year if present

#### ORG
- Include government agencies and institutional bodies
- Exclude generic mentions unless clearly identifiable

#### DATE
- Only label explicit dates
- Do not label vague temporal expressions (e.g., “today”, “recently”)

---

## 4. Edge Cases

- Case names (e.g., *Simmons v. United States*)  
  → Label PARTY entities separately, NOT as CITATION

- Inline legal references  
  → If in reporter format → CITATION  
  → Otherwise → NOT labeled

- Section headers or artifacts (e.g., single letters like "C")  
  → Ignore (label as O)

---

## 5. Annotation Philosophy

- Prioritize consistency over subjective interpretation
- When uncertain, choose the most conservative valid label
- Do not over-label ambiguous spans

---

## 6. Notes for Annotation

- The dataset contains mixed formatting and historical artifacts
- Some texts may include OCR noise or formatting irregularities
- Annotators should rely on semantic meaning rather than formatting

