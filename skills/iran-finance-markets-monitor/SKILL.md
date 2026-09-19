---
name: iran-finance-markets-monitor
description: "Use whenever a user asks to monitor, collect, validate, compare, summarize, or report Iranian financial markets, including USD/IRR or USD/Toman, EUR, AED, gold, Emami coin, Nima, USDT/Toman, crypto prices, Fear & Greed, TGJU, Nobitex, Wallex, Bitpin, or a Persian market report. Collect provenance-rich partial data, never invent missing values, and report source failures explicitly."
compatibility: "Python 3.10+; install dependencies from requirements.txt for live collection. Network access is required for live data."
metadata:
  version: 1.0.0
  tags: [finance, crypto, iran-market, tgju, scraping, monitoring, persian]
---

# Iranian Finance Markets Monitor

Use this skill to produce neutral, auditable snapshots and Persian-language market reports. It is a data-collection and explanation workflow, not investment advice or a trading signal.

## Safety and integrity rules

- Never provide personalized investment advice, guaranteed predictions, or fabricated prices.
- Preserve the original unit in provenance. TGJU values are commonly Rial; display Iranian retail values in Toman only after explicit division by 10.
- Every populated numeric field needs a source identifier. A missing value must remain `null` and its failure must appear in `errors` or `warnings`.
- Treat each source independently: a TGJU outage must not erase CoinGecko data, and a crypto outage must not erase FX/gold data.
- Clearly distinguish observed data, calculated values, validation failures, and neutral interpretation.

## Workflow

1. Confirm the requested time window, market scope, currency unit, and desired output language. If unspecified, use the latest available snapshot and Persian for the report.
2. Read `references/market-data-sources.md` before changing selectors or interpreting TGJU tables. Table positions are operational hints, not proof that a page has not changed.
3. For live collection, install `requirements.txt` and run the bundled watcher with `--stdout-only` for inspection or `--output-dir` for a dated JSON artifact.
4. Normalize Persian and Arabic digits, parse numbers conservatively, convert Rial to Toman exactly once, and apply range/freshness/reconciliation gates.
5. Return partial data when a source fails. Never substitute a guessed value, stale value, or unrelated source.
6. Generate the Persian report from `templates/market-report-fa.txt`; use `—` for null values and include the source/failure note when useful.
7. Add a short neutral summary describing direction, dispersion, and data quality—not a buy/sell recommendation.

## Data contract

The watcher emits JSON with:

- `schema_version`, `date_gregorian`, `date_jalali`, and an ISO-8601 `timestamp_tehran`.
- `status`: `ok` only when no errors were recorded; otherwise `partial`.
- `crypto`: BTC, ETH, USDT/Toman, selected alts, Fear & Greed, and total market cap.
- `iran_fx_gold`: free USD, EUR, AED, 18K gold, Emami coin, and Nima placeholder.
- `news`: at most three links, with source and URL; RSS is fallback-only when TGJU news is empty.
- `errors`: structured source, type, and detail records; `warnings`: non-fatal omissions.

Use the pure helpers in `scripts/iran_market_watcher.py` for tests and integrations: `normalize_digits`, `parse_number`, `rial_to_toman`, `validate_range`, `validate_freshness`, and `parse_table_row`.

## Validation gates

- Localized numeric parsing must support Persian/Arabic digits and separators.
- Price ranges are broad sanity bounds, not forecasts; rejected values stay null.
- TGJU date fields are accepted only for today through two days old unless the user explicitly requests historical data.
- USDT exchange quotes require valid buy/sell prices, each quote spread no greater than 0.5%, and cross-exchange dispersion no greater than 0.5%.
- CoinGecko and Fear & Greed responses require successful HTTP status and basic numeric sanity checks.
- Use Tehran’s IANA timezone (`Asia/Tehran`), not a permanently hard-coded UTC offset.

## Commands

From the repository root:

```bash
python3 -m pip install -r skills/iran-finance-markets-monitor/requirements.txt
python3 skills/iran-finance-markets-monitor/scripts/iran_market_watcher.py --stdout-only
python3 skills/iran-finance-markets-monitor/scripts/iran_market_watcher.py --output-dir ./data/market
python3 -m pytest skills/iran-finance-markets-monitor/tests -q
```

For restricted/offline environments, run the tests and pure helpers only. Do not claim that live prices were collected when network access or dependencies are unavailable.

## Reporting template

Use the bundled Persian template and fill missing values with `—`. Include:

- Jalali date and Tehran preparation time.
- BTC, ETH, USDT/Toman, and Fear & Greed where available.
- Free USD, EUR, AED, Emami coin, and 18K gold where available.
- One to three dated/source-linked headlines, with RSS marked as fallback.
- A two- or three-sentence neutral market summary and a data-quality note.

## Troubleshooting

- `jdatetime is required`: install the bundled requirements; Jalali dates must not be approximated.
- Few or changed TGJU tables: record a scrape/schema error and inspect the source reference; do not silently shift indices.
- Rate limiting or timeout: retry is bounded, then preserve partial output and record the failure.
- Persian values parse as null: test `normalize_digits` and `parse_number` with the exact source text before changing selectors.
