### TGJU (Iranian Market) Scraping

Target URL: `https://www.tgju.org/`

#### Table locations and drift policy

These indices are operational hints, not an API contract. Always verify the
table count and exact first-cell labels. If an expected table or label is
missing, record a schema error and leave the field null; never silently use a
neighboring table.

| Table Index | Label | Use |
|-------------|-------|-----|
| `0` | `سکه` | Gold 18K fallback, Emami Coin fallback |
| `5` | `قیمت طلا` | Gold 18K (primary) |
| `10` | `قیمت سکه` | Emami Coin (primary) |
| `14` | `ارز آزاد` | USD free, EUR, AED |
| `18` | `قیمت ارزهای دیجیتال` | BTC/ETH/USDT reference prices |
| `33` | `صرافی` | USDT/Toman cross-exchange reconciliation (Nobitex, Wallex, Bitpin) |

#### Parsing Logic

Search for table rows (`tr`) containing specific Persian keywords, but **always qualify with table index and exact first-cell label**:

| Keyword | Variable | Note |
|---------|----------|------|
| `"دلار"` in table 14 | Free USD | Do not use bare keyword matching; table 14 also contains EUR, AED, POUND |
| `"طلای 18 عیار"` in table 5 | 18K Gold | Primary source; table 0 is fallback |
| `"سکه امامی"` in table 10 | Emami Coin | Primary source; table 0 is fallback |
| `"تتر"` in table 33 | USDT/Toman | Prices are Rials; divide by 10 for Tomans |
| `"یورو"` in table 14 | EUR | Same table as USD free |
| `"درهم"` in table 14 | AED | Same table as USD free |

#### Rial to Toman

```python
price_rial = int(cols[1].replace(",", ""))
price_toman = price_rial // 10
```

#### Validation Gates

| Field | Range Check | Freshness | Cross-Source |
|-------|-------------|-----------|--------------|
| USD free (Toman) | Broad sanity range in the script | Today/1–2 days | Optional USDT proxy comparison |
| EUR (Toman) | Broad sanity range in the script | Today/1–2 days | Optional USD ratio comparison |
| AED (Toman) | Broad sanity range in the script | Today/1–2 days | Optional USD ratio comparison |
| Gold 18K (Toman) | Broad sanity range in the script | Today/1–2 days | Do not infer from news |
| Emami Coin (Toman) | Broad sanity range in the script | Today/1–2 days | Compare fallback only when collected |
| USDT/Toman | Broad sanity range in the script | Current quote | Quote and cross-exchange spread ≤0.5% |

These are anomaly gates, not investment forecasts. Update the script and tests
together when market regimes require a bound change.

#### News Sources

1. **Primary**: TGJU crypto news page `https://www.tgju.org/news/category/93966/` — extract links matching `/news/`.
2. **Fallback-only**: Cointelegraph RSS `https://cointelegraph.com/rss` — use it only when the TGJU news list is empty.
3. **Do not mix**: Never combine a category heading with a real news article in the same slot.
4. **Attribution**: Store title, source, and canonical URL; cap output at three links.
