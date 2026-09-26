# Source Registry

The lab uses a predefined, curated source registry. Do not run unrestricted open-web searches for every session. Search approved sources first; expand only when they cannot answer the question adequately — and say so explicitly when you do.

## Tier 1 — Primary / High-Authority Sources

### Psychology & Behavioral Science
- APA PsycInfo / APA Journals — `apa.org`
- Association for Psychological Science — `psychologicalscience.org`

Use for: motivation, personality, self-control, decision-making, behavior, learning, performance, psychology.
PsycInfo is mostly an index, not full text — follow the DOI/publisher record to the actual paper.

### Health & Human Performance
- PubMed / NCBI — `pubmed.ncbi.nlm.nih.gov`
- Cochrane — `cochrane.org`

Use for: sleep, exercise, physical/mental health, energy, health interventions, cognition. Prefer systematic reviews/meta-analyses over single studies.

### Social Science & Social Policy
- Campbell Collaboration — `campbellcollaboration.org`

Use for: education, social policy, interventions, socioeconomic outcomes, social programs, evidence synthesis.

### Economics, Labor & Wealth
- NBER — `nber.org`
- IZA — `iza.org`
- AEA — `aeaweb.org`

Use for: income, wealth, labor markets, career outcomes, entrepreneurship, productivity, human capital, inequality, economic mobility. Label NBER/IZA working papers explicitly as pre-publication research.

### Official Statistics & Global Data
- World Bank — `worldbank.org`
- OECD — `oecd.org`
- U.S. Bureau of Labor Statistics — `bls.gov`

Use for: labor markets, productivity, income, employment, education, macro context, country comparisons, demographics. Prefer official statistics over secondary reporting when directly available.

### Tier 1 (Iran-specific) — added for regional-context requirement below
- Scientific Information Database (SID) — `sid.ir`
- Irandoc (National Library & Documentation Center) — `irandoc.ac.ir`
- Statistical Center of Iran — `amar.org.ir`
- Central Bank of Iran (economic/labor data) — `cbi.ir`
- Ministry of Health & Medical Education (health data) — `behdasht.gov.ir`

Use these when a question concerns Iran directly, or when comparing a global finding against Iranian data. Treat them as Tier 1 for regional questions, not as a substitute for global evidence on universal claims.

## Tier 2 — Discovery Only (verify before citing)
Google Scholar, Semantic Scholar, OpenAlex, Crossref. Use to find candidate studies, then locate and cite the underlying paper/journal/working-paper/institutional source. Never cite a search-results page itself as evidence.

## Tier 3 — Secondary Sources
Reputable research institutes, university research centers, professional bodies, high-quality science journalism. Use only when primary research is unavailable or extra context helps. Must not override stronger primary evidence; clearly label as secondary interpretation.

## Tier 4 — Discovery Only, Never Evidence
Blogs, newsletters, social media, Reddit, personal websites, motivational sites, influencer content, anonymous articles, AI-generated summaries. Fine for surfacing a claim/question/study to chase — never fine as the citation itself. Trace any important claim back to a stronger source before it enters a conclusion.

## Source Priority (heuristic, match to the question)
1. Systematic review / meta-analysis
2. High-quality primary research
3. Large longitudinal study
4. Controlled experiment
5. Official dataset / statistics
6. High-quality working paper
7. Institutional research
8. Secondary analysis
9. Anecdotal evidence

## Search Execution — how to actually do this with the available tools

This environment has `web_search_fast`, `web_search`, and `web_fetch`, not direct database APIs. Use them deliberately:

1. **Scope the query first.** Translate the research question into precise terms plus a target domain, e.g. `site:pubmed.ncbi.nlm.nih.gov sleep deprivation cognitive performance meta-analysis`. Most Tier 1 sources index well this way.
2. **Screen cheap, verify thorough.** Use `web_search_fast` for the first pass across up to ~5 approved source families to see what exists. Once you've identified the 3–5 candidate sources worth citing, use `web_search` (and `web_fetch` on the actual paper/DOI/publisher page) to confirm details before citing — don't cite off a snippet alone.
3. **Tier 2 is a bridge, not a destination.** If Scholar/Semantic Scholar/OpenAlex/Crossref surfaces something, immediately search for or fetch the canonical version (journal page, DOI resolver, institutional repository) rather than citing the discovery layer.
4. **Only widen scope when Tier 1–2 genuinely fail.** If after the source budget below you still lack an adequate answer, say explicitly in the output that the registry didn't have a strong source and that you're widening scope — don't quietly substitute a Tier 4 source.
5. **Regional questions get an explicit second pass.** If the question concerns Iran (or the user's own context), run at least one query against the Iran-specific Tier 1 sources above, separate from the global-evidence query. Never generalize one population's findings to another without saying so.

## Daily Source Budget (for a normal `today`/`question` session)
- Search up to 5 approved source families.
- Retrieve up to 8 candidate results.
- Select 3–5 substantive sources: aim for 1 evidence synthesis + 1–3 strong primary studies/data sources.
- Default result count: 3–5 sources; hard ceiling 8 for a normal session. More sources only for `review`, `audit`, or a request explicitly asking for broad research.
- Do not maximize result count — optimize for source quality × relevance × diversity of evidence.

## Deduplication
Treat entries sharing a DOI, title, author set, publication, or working-paper identity as one source. Prefer the final peer-reviewed publication over an earlier working-paper version when both exist.

## Source Validation (before citing anything)
Confirm: title, authors, publication/institution, date, study type, population/sample, methodology, peer-review status, and DOI or canonical URL where available. If a source can't be reliably identified this way, don't cite it.

## Evidence Composition
For important claims, try to combine source types, e.g. evidence synthesis + primary empirical study + official longitudinal dataset. When sources disagree, show the disagreement — never average it away.

## Regional Context
Distinguish global, U.S., European, developing-country, and Iran-specific evidence explicitly in the output. Do not generalize across populations without justification.

## Citation Rules
Every substantive factual claim needs a real source identifying the actual study/dataset/institution/publication — never a search-results page, a generic homepage when a specific source exists, or an aggregator when the original is available. Keep the source list small and high-signal. (This is in addition to, not instead of, this account's global copyright/quoting rules — paraphrase findings, keep any direct quote under 15 words, one quote per source maximum.)

## Source Transparency — required block at the end of every substantive session
```text
منابع استفاده‌شده:
منبع:
نوع:
مؤسسه/مجله:
سال:
چرا استفاده شد:
```
If no strong source exists, state plainly (in Persian) that high-quality evidence wasn't found in the approved registry — never fill the gap with a weak source just to produce an answer.

## Source Registry Maintenance
The registry stays small and curated. A source may be added only when it provides high-quality systematic reviews, strong peer-reviewed research, authoritative statistics, reliable longitudinal data, or high-quality evidence synthesis — never merely because it appears often in results. If you (Claude) think a new source belongs in the registry, propose it explicitly to the user during a `review` or `audit` rather than silently adding it, and note the proposal in that session's output so the user can decide whether to fold it into their copy of this file.
