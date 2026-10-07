# Iran Finance Markets Monitor

Monitor Iranian financial markets — USD/IRR, gold, crypto, Fear & Greed.

## Installation

```bash
pip install -r skills/iran-finance-markets-monitor/requirements.txt
```

## Usage

```bash
python3 skills/iran-finance-markets-monitor/scripts/iran_market_watcher.py --stdout-only
python3 skills/iran-finance-markets-monitor/scripts/iran_market_watcher.py --output-dir ./data/market
```

## Safety

- Never provides investment advice
- Preserves original units (Rial vs Toman)
- Reports source failures explicitly
- Returns partial data when a source fails

See `SKILL.md` for full documentation.
