# Persian Success Lab

A long-running, evidence-based research-and-experiment system for one question:

> What actually causes people to become successful, and what reliably improves my own outcomes?

This is **not** a motivation or self-help skill. It enforces a strict evidence hierarchy, a curated source registry, and mandatory Persian-language output. Its goal is not to collect interesting facts — it's to **change the model**: revise a belief, test an assumption, find a variable that matters, or learn what actually works.

## Core Principles

- **No universal formula.** Success is decomposed into individual, strategy, social, and external factors, each with its own constraints, trade-offs, and context.
- **Evidence before opinion.** Every substantive claim is traced to a real study, dataset, or institution — never to a blog, a search-results page, or a famous person's story.
- **Correlation is not causation.** Each session actively checks for survivorship bias, selection effects, publication bias, confounders, reverse causality, and effect size.
- **Personal results are not proof.** A personal experiment is one input, not a verdict.
- **The model is the deliverable.** The log is history; the model is the current best guess, revised every session.

## Evidence Hierarchy

Strongest first. Match evidence type to the question — newer is not automatically better.

```text
Meta-analyses → Systematic reviews → High-quality peer-reviewed studies
→ Large longitudinal studies → RCTs / controlled experiments
→ High-quality datasets → Strong institutional research → Expert synthesis
→ Books → Interviews / anecdotes
```

## Operating Modes

One mode per invocation.

| Command | What It Does |
|---------|--------------|
| `today` | Full research session: one narrow question → source-registry research → findings → uncertainty → one hypothesis → one small experiment → measurement → log entry |
| `question <topic>` | Deep research on a specific topic. Proposes an experiment only if one naturally follows |
| `experiment <hypothesis>` | Turns an existing hypothesis into a small, specific, reversible, cheap, measurable, time-bounded experiment |
| `review` | Cross-session synthesis: recurring factors, contradictions, failed hypotheses, weak assumptions. Updates the model. Run as a Weekly Synthesis at least every 7 sessions |
| `dashboard` | Plain counts and lists: sessions, experiments by status, validated/rejected hypotheses, open questions, recurring variables, strong vs. weak evidence. **Never** a score, grade, or ranking of the user |
| `audit` | Attacks the current model: what could be wrong, what's correlation read as causation, what's anecdote-driven, what would falsify current beliefs |

## Research Framework

Every session keeps these separate, in order:

```text
Evidence → Interpretation → Hypothesis → Personal experiment → Personal result
```

Questions rotate across ten domains — Skill, Career, Wealth, Productivity, Psychology, Health, Social Capital, Environment, Strategy, Luck — and the session log records which domain was covered.

Question quality matters:

- Weak: "How do successful people think?"
- Better: "Does structured goal-setting improve completion of complex tasks?"
- Best: "Under what conditions does structured goal-setting improve completion of complex tasks?"

Popular myths ("10,000 hours", "wake at 5 AM", "follow your passion") are stress-tested rather than assumed true or false.

## Language Rules

- The skill's own files, schemas, and structure stay in **English**.
- **All user-facing content is Persian (Farsi)**: questions, summaries, hypotheses, experiments, results, reviews, model updates, logs, and source-transparency blocks.
- Sources may be read in any language, but findings are synthesized and presented in Persian.
- Technical terms, proper nouns, paper titles, DOIs, and journal names stay in their original form when translation would reduce precision.

## State & Persistence

The lab is meant to accumulate across sessions, with two **separate** artifacts:

- **Research/experiment log** — chronological history of every session and experiment
- **Model file** — the current synthesized set of beliefs, revised over time

Persistence depends on the environment:

- **Durable location available** (Claude Code / Cowork project directory, connected Drive or Notion doc, re-uploaded files): read the existing log and model before any `today`, `review`, `dashboard`, or `audit`, then update them in place.
- **No durable location** (plain claude.ai chat with nothing uploaded): say so at the start, then output the full, updated content of every changed file in a copy-pasteable block at the end of each session.

The skill never silently assumes state that wasn't actually provided in the conversation.

## Output Format

Daily sessions use a fixed, compact Persian structure — no motivational filler, no manufactured certainty:

```text
### سوال امروز
### شواهد چه می‌گویند
### آنچه هنوز نامشخص است
### فرضیه
### آزمایش امروز
### معیار سنجش
### ثبت در لاگ
```

Every substantive session ends with a source-transparency block (منابع استفاده‌شده: منبع / نوع / مؤسسه یا مجله / سال / چرا استفاده شد). When no strong source exists, the skill says so instead of substituting a weak one.

## File Structure

```text
persian-success-lab/
├── SKILL.md                        # Skill definition and operating modes
└── references/
    ├── source-registry.md          # Approved sources, tiers, search budget — read before any research
    ├── record-schemas.md           # Research Record and Experiment Record templates
    └── success-model.md            # Domain rotation, hypothesis map, Weekly/Monthly review formats
```

- **`source-registry.md`** — Tier 1 primary sources (APA, PubMed/Cochrane, NBER/IZA/AEA, World Bank/OECD, Campbell Collaboration, and Iran-specific sources such as SID, Irandoc, the Statistical Center of Iran, CBI, and the Ministry of Health), plus Tier 2 discovery-only, Tier 3 secondary, and Tier 4 discovery-only-never-evidence. Includes a search budget: up to 5 source families, up to 8 candidate results, 3–5 substantive sources per session.
- **`record-schemas.md`** — field-level templates for every research and experiment entry.
- **`success-model.md`** — the ten-domain rotation list, the living hypothesis map, and the Weekly Synthesis / Monthly Model Review / Dashboard formats.

## Installation

### skills.sh

```bash
npx skills add ehsanghaffar/skills --skill persian-success-lab
```

### Claude Code

```bash
cp -r skills/persian-success-lab ~/.claude/skills/
```

### claude.ai

Add the skill to project knowledge, or paste the contents of `SKILL.md` into the conversation. For file-based setups, the three `references/` files must be reachable too — the skill reads `source-registry.md` before any research task.

## Network Access

This skill requires web search. Grant access to the research domains it uses, including:

- `apa.org`, `psychologicalscience.org`
- `pubmed.ncbi.nlm.nih.gov`, `cochrane.org`
- `nber.org`, `iza.org`, `aeaweb.org`
- `worldbank.org`, `oecd.org`, `bls.gov`
- `campbellcollaboration.org`
- `sid.ir`, `irandoc.ac.ir`, `amar.org.ir`, `cbi.ir`, `behdasht.gov.ir`
- `scholar.google.com`, `semanticscholar.org`, `openalex.org`, `crossref.org`

In claude.ai, add the required domains at **claude.ai/settings/capabilities**. Without them the skill can reason about the framework but cannot ground a session in real sources — and it will say so rather than inventing them.

## Important Notes

- **One mode per invocation** unless you explicitly chain them.
- **Question rotation matters** — repeating one domain for weeks makes the model shallow and self-confirming.
- **Failed experiments count.** If an experiment eliminates or weakens a hypothesis, that is a result worth recording, not a non-event.
- **No numerical scoring.** Confidence is expressed qualitatively (strong / moderate / weak / unknown) unless the underlying evidence genuinely supports quantitative scoring.
- **Population boundaries are explicit.** Global, U.S., European, developing-country, and Iran-specific evidence are distinguished rather than blurred together.
- **Registry changes are proposed, not silent.** New sources must be suggested to you during a `review` or `audit` before entering your copy of `source-registry.md`.
