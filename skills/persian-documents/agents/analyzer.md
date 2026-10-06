# Analyzer Instructions for Persian Document Generator

This analyzer examines benchmark results to identify patterns and improvement opportunities.

## What to look for

### 1. Non-discriminating assertions
If an assertion passes for both with-skill and without-skill runs, it's not discriminating. Consider:
- Is the assertion too easy?
- Does it test something the baseline already handles?
- Should the assertion be made more specific?

### 2. High-variance evals
If an eval has high variance across runs, it may be flaky. Look for:
- Inconsistent scoring between runs
- Different failure modes each time
- Sensitivity to small input changes

### 3. Skill-specific improvements
Patterns that indicate the skill needs improvement:
- Multiple runs fail on the same criterion
- Common RTL issues appear across evals
- Mixed-direction content consistently problematic
- Typography errors recurring

### 4. Baseline patterns
If baseline runs also pass some assertions:
- The skill may not be adding value for those cases
- The baseline model may already handle some RTL correctly
- Consider adjusting the skill to focus on harder cases

## Analysis framework

For each eval, answer:

1. **What failed?** — Which assertions did not pass?
2. **Why did it fail?** — Root cause analysis
3. **Is this skill-specific?** — Would improving the skill fix this?
4. **What's the fix?** — Specific skill changes needed

## Report format

```
## Analysis for eval: [name]

### Failed assertions
- [assertion name]: [description of failure]

### Root cause
[Explanation of why the failure occurred]

### Skill improvement
[Specific changes to make to the skill]

### Baseline observation
[Whether baseline also failed, and what that means]
```

## Key patterns to identify

| Pattern | Likely Cause | Skill Fix |
|---------|--------------|-----------|
| Reversed English | Model not using logical order | Emphasize logical order principle |
| Broken URLs | URL reordering | Add URL handling rules |
| Scrambled versions | Number direction issue | Add version number rules |
| Wrong glyphs | Font/character issue | Add glyph guidance |
| LTR paragraphs | Direction not set | Add paragraph direction rules |
| Table column order | Table direction missing | Add table RTL rules |
