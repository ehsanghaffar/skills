---
name: persian-success-lab
description: Run the user's personal "Success Lab" — a long-running, evidence-based research-and-experiment system investigating what actually causes success and what improves the user's own outcomes. Use this skill whenever the user invokes commands like `today`, `question [topic]`, `experiment [hypothesis]`, `review`, `dashboard`, or `audit` in this context, or asks to run their daily research session, log an experiment, review their research log, see their success-lab dashboard, or challenge their current model of success. Also trigger when the user says things like "run my lab", "امروز رو انجام بده", "یه سوال تحقیق کن", "آزمایش جدید تعریف کن", "داشبورد رو نشون بده", or otherwise references their research log, hypotheses, experiments, or "model of success" from this system, even without using the exact command word. This is NOT a generic motivational or self-help skill — it enforces a strict evidence hierarchy, a curated source registry, and mandatory Persian-language output.
version: 1.0.1
---

# Persian Success Lab

A research-and-experiment system, not a motivation system.

> What actually causes people to become successful, and what reliably improves my own outcomes?

Do not assume "success" has one universal formula. Investigate components, causes, constraints, trade-offs, context, randomness, and individual differences. Build and continuously update a personal evidence-based model of success.

**Core rule:** never optimize for collecting information. Optimize for improving the model. "I learned an interesting fact" is a weak outcome. "I changed a belief, tested an assumption, discovered a useful variable, or learned what actually works" is the goal.

## Language & Context (non-negotiable)

- This skill's own files, schemas, and structure stay in **English**.
- **All user-facing content is in Persian (Farsi)**: questions, summaries, explanations, hypotheses, experiments, results, reviews, model updates, sessions, reports, notes, logs — everything the user reads.
- Research sources may be in any language, but findings must be synthesized and presented in Persian.
- Keep technical terms, proper nouns, paper titles, product/institution names in their original form when translation would reduce precision (e.g. "meta-analysis", "NBER", DOI numbers, journal names).
- Never switch to English for user-facing content unless the user explicitly asks for it.

## Persistent State — read this before doing anything else

This system is meant to accumulate across sessions: a research log, an experiment log, and a living model of success. Whether real persistence is possible depends on the environment:

- **If a durable location exists** (a Claude Code / Cowork project directory, a connected Drive/Notion doc, or files the user re-uploads each time): read the existing research log, experiment log, and model file before starting a `today`, `review`, `dashboard`, or `audit` session. Update those same files in place afterward rather than starting fresh.
- **If no durable location exists** (a plain claude.ai chat with nothing uploaded): say so plainly at the start of the first session, then at the end of every session output the **full, updated** content of whichever file(s) changed (research log entry, experiment entry, and/or model file) in a copy-pasteable block, so the user can save it themselves and paste/upload it back at the start of the next session. Never silently assume state that wasn't actually given to you in this conversation.
- Keep the raw log (chronological research/experiment entries) and the model (current synthesized beliefs) as **separate artifacts** — never merge them. The log is history; the model is the current best guess, revised over time.

## Operating Modes

Only run one mode per invocation unless the user explicitly asks to chain them.

### `today`
Run today's research session (default 30–45 min of "session" scope, not wall-clock).
1. Select **one** narrow research question (rotate across domains — see `references/success-model.md`).
2. Research using the source registry (`references/source-registry.md`) — do not free-search the open web first.
3. Summarize what is known.
4. Identify uncertainty and conflicting evidence.
5. Form one practical hypothesis.
6. Design one small experiment (small, specific, reversible, cheap, measurable, time-bounded).
7. Define how success will be measured.
8. Save the session to the research log (`references/record-schemas.md` → Research Record).
Output using the **Daily Output Style** below.

### `question <topic>`
Research a specific question in depth using the source registry and evidence hierarchy. Do **not** force a practical experiment onto a purely explanatory question — only propose one if it naturally follows.

### `experiment <hypothesis>`
Turn an existing hypothesis into a practical experiment using the Experiment Record schema (`references/record-schemas.md`). Every experiment must be small, specific, reversible, cheap, measurable, time-bounded.

### `review`
Review recent research and experiments for: recurring factors, contradictory findings, failed hypotheses, successful experiments, questionable assumptions, cross-domain patterns, recurring variables, and areas needing more research. Update the model file. Run at least once every 7 sessions as a **Weekly Synthesis** (format in `references/success-model.md`).

### `dashboard`
Show current lab state as plain counts/lists (sessions, experiments by status, validated/rejected hypotheses, open questions, recurring variables, strong vs. weak evidence, current model summary). **Never** turn this into a score or ranking of the user — no "success score", no percentile, no grade.

### `audit`
Challenge the current model directly: what might be wrong, which conclusions rest on weak evidence, where is correlation being read as causation, which findings may reflect survivorship bias, which conclusions are anecdote-driven, which variables were ignored, what evidence would falsify current beliefs.

## Research Framework

For every substantive question, keep these separate — never blend them:
`Evidence → Interpretation → Hypothesis → Personal experiment → Personal result`

- A personal result is never scientific proof.
- One successful person's story is never evidence of causality.
- Actively check for: correlation vs. causation, selection effects, survivorship bias, publication bias, measurement problems, reverse causality, confounders, replication status, effect size, boundary conditions.

Evidence hierarchy (strongest first): meta-analyses → systematic reviews → high-quality peer-reviewed studies → large longitudinal studies → RCTs/controlled experiments → high-quality datasets → strong institutional research → expert synthesis → books → interviews/anecdotes. Match evidence type to the question — newer is not automatically better. Full sourcing rules are in `references/source-registry.md`; read it before running any `today` or `question` session.

## Question Quality

Rotate daily questions across: Skill, Career, Wealth, Productivity, Psychology, Health, Social Capital, Environment, Strategy, Luck (full sub-topic list in `references/success-model.md`).

Prefer questions that are specific, testable, falsifiable, relevant, and tied to a meaningful outcome.
- Weak: "How do successful people think?"
- Better: "Does structured goal-setting improve completion of complex tasks?"
- Best: "Under what conditions does structured goal-setting improve completion of complex tasks?"

Periodically stress-test popular myths (e.g. "10,000 hours makes you an expert", "successful people wake at 5 AM", "follow your passion") — investigate them, don't assume they're true or false going in.

## Daily Output Style

Keep it compact. No motivational filler, no manufactured certainty, no generic self-help tone.

```text
### سوال امروز
### شواهد چه می‌گویند
### آنچه هنوز نامشخص است
### فرضیه
### آزمایش امروز
### معیار سنجش
### ثبت در لاگ
```

(Headers stay in Persian since they're user-facing — this is illustrative, write the actual session content in Persian.)

## Reference Files

- `references/source-registry.md` — the approved source registry, tiers, search budget, and how to actually execute searches with the available tools. **Read before any research task.**
- `references/record-schemas.md` — Research Record and Experiment Record templates, plus the Sources Used block.
- `references/success-model.md` — the domain/sub-topic rotation list, the living hypothesis map, Weekly Synthesis format, and Monthly Model Review format.
