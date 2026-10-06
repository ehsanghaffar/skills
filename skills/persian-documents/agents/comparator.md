# Comparator Instructions for Blind A/B Comparison

This comparator evaluates two versions of a Persian document generator skill without knowing which is which.

## Input

You will receive two outputs (A and B) for the same prompt. Do NOT ask which is which.

## Evaluation criteria

Rate each output on a 1-5 scale:

### 1. RTL Correctness (1-5)
- 5: Perfect RTL layout, no issues
- 4: Minor RTL issues, mostly correct
- 3: Noticeable RTL issues but readable
- 2: Significant RTL problems
- 1: Completely wrong direction

### 2. Mixed-Direction Content (1-5)
- 5: English/Persian mixed perfectly
- 4: Minor issues with mixed content
- 3: Some mixed content problems
- 2: Mixed content hard to read
- 1: Mixed content completely broken

### 3. Typography (1-5)
- 5: Perfect Persian typography
- 4: Minor typography issues
- 3: Noticeable typography problems
- 2: Poor typography
- 1: Unreadable typography

### 4. Professional Quality (1-5)
- 5: Production-quality document
- 4: Good quality, minor issues
- 3: Acceptable but needs work
- 2: Below professional standard
- 1: Not usable

## Output format

```json
{
  "winner": "A" | "B" | "tie",
  "scores": {
    "A": {"rtl": 4, "mixed": 5, "typography": 4, "professional": 4},
    "B": {"rtl": 3, "mixed": 4, "typography": 3, "professional": 3}
  },
  "reasoning": "Explanation of why A won",
  "specific_issues": [
    "Issue 1 in B",
    "Issue 2 in A"
  ]
}
```

## Important rules

- Do NOT ask which output is from which version
- Judge purely on output quality
- Consider the document as a whole
- Focus on RTL correctness and mixed-direction handling
- Note specific, actionable issues
