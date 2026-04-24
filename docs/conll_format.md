# CoNLL Format Specification

This project uses a 6-column CoNLL-style format.

## Columns

1. token          - surface word
2. pos            - part-of-speech tag
3. chunk          - chunk tag (NP/VP/...)
4. shape          - word shape feature (e.g., Xxxx, XX, dddd)
5. stage2_tag     - rule-based tag (BIO format)
6. gold_tag       - final human annotation (BIO format)

## Example

John    NNP   B-NP   Xxxx   B-PER   B-PER
Smith   NNP   I-NP   Xxxxx  I-PER   I-PER
works   VBZ   B-VP   xxxx   O       O

## Rules

- Sentences are separated by blank lines
- stage2_tag defaults to O before rule-based tagging
- gold_tag is filled only after annotation
- All downstream modules MUST follow this exact format
