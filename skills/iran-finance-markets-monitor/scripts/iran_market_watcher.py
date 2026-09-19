#!/usr/bin/env python3
"""Collect a partial, provenance-rich snapshot of Iranian and crypto markets."""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

try:
    import feedparser
except ImportError:
    feedparser = None
try:
    import jdatetime
except ImportError:
    jdatetime = None
try:
    import requests
except ImportError:
    requests = None
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

LOG = logging.getLogger("iran-market-watcher")
TEHRAN = ZoneInfo("Asia/Tehran")
DEFAULT_MARKET_DATA_DIR = os.environ.get("MARKET_DATA_DIR", "./data/market")
USER_AGENT = "iran-finance-markets-monitor/2.0"
RANGES = {
    "usdt_toman": (100_000, 1_000_000), "usd_free": (100_000, 1_000_000),
    "eur": (100_000, 1_500_000), "aed": (20_000, 300_000),
    "gold_18k": (5_000_000, 100_000_000), "sekkeh_emami": (50_000_000, 1_000_000_000),
}


def normalize_digits(value: Any) -> str:
    """Convert Persian/Arabic numerals and localized separators to ASCII text."""
    text = "" if value is None else str(value)
    translation = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    return text.translate(translation).replace("٬", ",").replace("٫", ".")


def parse_number(value: Any, *, integer: bool = True) -> int | float | None:
    """Parse a localized number; return None for missing or malformed input."""
    text = normalize_digits(value).strip()
    if not text or text in {"-", "—", "نا مشخص", "نامشخص"}:
        return None
    match = re.search(r"[-+]?\d+(?:[,.]\d+)?", text.replace(",", ""))
    if not match:
        return None
    try:
        number = float(match.group(0))
        return int(number) if integer else number
    except ValueError:
        return None


def now_tehran() -> datetime:
    return datetime.now(timezone.utc).astimezone(TEHRAN)


def jalali_date(value: datetime | None = None) -> str:
    if jdatetime is None:
        raise RuntimeError("jdatetime is required for Jalali dates")
    value = value or now_tehran()
    local = value.astimezone(TEHRAN).replace(tzinfo=None)
    return jdatetime.datetime.fromgregorian(datetime=local).strftime("%Y/%m/%d")


def validate_freshness(date_text: str, today_jalali: Any, max_age_days: int = 2) -> tuple[bool, str]:
    """Accept source dates from today through ``max_age_days`` ago."""
    if jdatetime is None:
        return False, "jdatetime unavailable"
    match = re.search(r"(\d{4})\s*[/\-]\s*(\d{1,2})\s*[/\-]\s*(\d{1,2})", normalize_digits(date_text))
    if not match:
        return False, "no date"
    try:
        observed = jdatetime.date(*map(int, match.groups()))
        today = today_jalali.date() if hasattr(today_jalali, "date") else today_jalali
        age = (today - observed).days
    except (TypeError, ValueError):
        return False, "invalid date"
    if 0 <= age <= max_age_days:
        return True, "today" if age == 0 else f"{age}days"
    return False, f"age {age} days exceeds {max_age_days}"


def validate_range(name: str, value: Any) -> tuple[bool, str]:
    number = parse_number(value, integer=False)
    bounds = RANGES.get(name)
    if number is None:
        return False, "missing or non-numeric"
    if bounds and not bounds[0] <= number <= bounds[1]:
        return False, f"{number} outside {bounds[0]}..{bounds[1]}"
    return True, "ok"


def rial_to_toman(value: Any) -> int | None:
    parsed = parse_number(value)
    return parsed // 10 if parsed is not None else None


def parse_table_row(table: Any, labels: Iterable[str]) -> list[str] | None:
    """Find a row whose first cell exactly matches one of ``labels``."""
    wanted = {normalize_digits(label).strip() for label in labels}
    for row in table.find_all("tr"):
        cells = [cell.get_text(" ", strip=True) for cell in row.find_all(["td", "th"])]
        if cells and normalize_digits(cells[0]).strip() in wanted:
            return cells
    return None


def request_text(url: str, *, timeout: int = 15, attempts: int = 3, headers: dict[str, str] | None = None) -> str:
    if requests is None:
        raise RuntimeError("requests is required for network collection")
    last_error: Exception | None = None
    request_headers = {"User-Agent": USER_AGENT, **(headers or {})}
    for attempt in range(attempts):
        try:
            response = requests.get(url, headers=request_headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except Exception as exc:
            last_error = exc
            if attempt + 1 < attempts:
                LOG.warning("request failed (%s/%s) %s: %s", attempt + 1, attempts, url, exc)
    raise RuntimeError(f"request failed after {attempts} attempts: {url}: {last_error}")


def empty_snapshot(timestamp: datetime) -> dict[str, Any]:
    return {
        "schema_version": "2.0", "date_jalali": jalali_date(timestamp),
        "date_gregorian": timestamp.date().isoformat(), "timestamp_tehran": timestamp.isoformat(),
        "status": "partial", "crypto": {
            "btc": {"price_usd": None, "change_24h": None, "volume": None, "source": None},
            "eth": {"price_usd": None, "change_24h": None, "volume": None, "source": None},
            "usdt_toman": {"price": None, "change": None, "source": None}, "top_alts": [],
            "fear_greed": {"value": None, "label": None, "source": None},
            "total_market_cap": {"value": None, "change_24h": None, "source": None},
        },
        "iran_fx_gold": {key: {"price": None, "change": None, "source": None} for key in (
            "usd_free", "eur", "aed", "gold_18k", "sekkeh_emami", "nima_rate")},
        "news": [], "errors": [], "warnings": [],
    }


def set_validated_price(snapshot: dict[str, Any], section: str, key: str, value: Any, source: str) -> None:
    valid, reason = validate_range(key, value)
    if not valid:
        snapshot["errors"].append({"field": key, "type": "range", "detail": reason, "source": source})
        return
    snapshot[section][key]["price"] = int(value)
    snapshot[section][key]["source"] = source


def fetch_market_data() -> dict[str, Any]:
    timestamp = now_tehran()
    data = empty_snapshot(timestamp)
    try:
        params = {"ids": "bitcoin,ethereum,tether,solana,binancecoin,ripple", "vs_currencies": "usd", "include_24hr_change": "true", "include_24hr_vol": "true"}
        response = requests.get("https://api.coingecko.com/api/v3/simple/price", params=params, headers={"User-Agent": USER_AGENT}, timeout=15) if requests else None
        if response is None:
            raise RuntimeError("requests is required")
        response.raise_for_status()
        quotes = response.json()
        for asset, target in (("bitcoin", "btc"), ("ethereum", "eth")):
            quote = quotes.get(asset, {})
            data["crypto"][target] = {"price_usd": quote.get("usd"), "change_24h": quote.get("usd_24h_change"), "volume": quote.get("usd_24h_vol"), "source": "CoinGecko /simple/price"}
        for asset, name in (("solana", "Solana"), ("binancecoin", "BNB"), ("ripple", "XRP")):
            if asset in quotes:
                data["crypto"]["top_alts"].append({"name": name, "price_usd": quotes[asset].get("usd"), "change_24h": quotes[asset].get("usd_24h_change"), "source": "CoinGecko /simple/price"})
    except Exception as exc:
        data["errors"].append({"source": "CoinGecko /simple/price", "type": "network", "detail": str(exc)})
    try:
        response = requests.get("https://api.coingecko.com/api/v3/global", headers={"User-Agent": USER_AGENT}, timeout=15) if requests else None
        if response is None:
            raise RuntimeError("requests is required")
        response.raise_for_status()
        value = response.json().get("data", {})
        data["crypto"]["total_market_cap"] = {"value": value.get("total_market_cap", {}).get("usd"), "change_24h": value.get("market_cap_change_percentage_24h_usd"), "source": "CoinGecko /global"}
    except Exception as exc:
        data["errors"].append({"source": "CoinGecko /global", "type": "network", "detail": str(exc)})
    try:
        response = requests.get("https://api.alternative.me/fng/", timeout=15) if requests else None
        if response is None:
            raise RuntimeError("requests is required")
        response.raise_for_status()
        item = (response.json().get("data") or [{}])[0]
        value = parse_number(item.get("value"))
        if value is None or not 0 <= value <= 100:
            raise ValueError("fear & greed value outside 0..100")
        data["crypto"]["fear_greed"] = {"value": value, "label": item.get("value_classification"), "source": "Alternative.me /fng"}
    except Exception as exc:
        data["errors"].append({"source": "Alternative.me /fng", "type": "network", "detail": str(exc)})
    try:
        html = request_text("https://www.tgju.org/")
        if BeautifulSoup is None:
            raise RuntimeError("beautifulsoup4 is required")
        tables = BeautifulSoup(html, "html.parser").find_all("table")
        if len(tables) <= 14:
            raise ValueError(f"TGJU returned {len(tables)} tables; expected at least 15")
        for index, labels, field in ((14, ("دلار",), "usd_free"), (14, ("یورو",), "eur"), (14, ("درهم",), "aed"), (10, ("سکه امامی",), "sekkeh_emami"), (5, ("طلای 18 عیار", "طلای ۱۸ عیار"), "gold_18k")):
            row = parse_table_row(tables[index], labels)
            price = rial_to_toman(row[1]) if row and len(row) > 1 else None
            if price is not None:
                set_validated_price(data, "iran_fx_gold", field, price, f"TGJU table {index}")
        if len(tables) > 33:
            mids = []
            for row in tables[33].find_all("tr"):
                cells = [cell.get_text(" ", strip=True) for cell in row.find_all(["td", "th"])]
                if len(cells) >= 4 and normalize_digits(cells[0]).strip() in {"نوبیتکس", "والکس", "بیت پین", "بیت‌پین"}:
                    buy, sell = parse_number(cells[1]), parse_number(cells[2])
                    if buy and sell and abs(buy - sell) / ((buy + sell) / 2) <= 0.005:
                        mids.append((buy + sell) / 2 / 10)
            if mids:
                spread = (max(mids) - min(mids)) / statistics.mean(mids)
                if spread <= 0.005:
                    set_validated_price(data, "crypto", "usdt_toman", round(statistics.mean(mids)), "TGJU table 33 exchange median")
                else:
                    data["errors"].append({"source": "TGJU table 33", "type": "reconciliation", "detail": f"exchange spread {spread:.2%} exceeds 0.50%"})
            else:
                data["warnings"].append("No valid USDT exchange quotes")
        else:
            data["warnings"].append("TGJU exchange table unavailable")
    except Exception as exc:
        data["errors"].append({"source": "TGJU", "type": "scrape", "detail": str(exc)})
    try:
        if requests is None:
            raise RuntimeError("requests is required")
        response = requests.get("https://www.tgju.org/news/category/93966/", headers={"User-Agent": USER_AGENT}, timeout=15)
        response.raise_for_status()
        if BeautifulSoup is None:
            raise RuntimeError("beautifulsoup4 is required")
        soup = BeautifulSoup(response.text, "html.parser")
        for anchor in soup.find_all("a", href=re.compile(r"/news/")):
            title = anchor.get_text(" ", strip=True)
            if len(title) >= 10:
                data["news"].append({"title": title, "source": "TGJU crypto news", "impact": "medium", "url": urljoin("https://www.tgju.org", anchor.get("href", ""))})
                if len(data["news"]) == 3:
                    break
    except Exception as exc:
        data["warnings"].append(f"TGJU news unavailable: {exc}")
    if not data["news"] and feedparser is not None:
        try:
            feed = feedparser.parse("https://cointelegraph.com/rss")
            data["news"] = [{"title": entry.title, "source": "Cointelegraph RSS", "impact": "medium", "url": entry.link} for entry in feed.entries[:3] if getattr(entry, "title", None)]
        except Exception as exc:
            data["errors"].append({"source": "Cointelegraph RSS", "type": "network", "detail": str(exc)})
    elif not data["news"]:
        data["warnings"].append("No news source available")
    data["news"] = data["news"][:3]
    data["status"] = "ok" if not data["errors"] else "partial"
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=DEFAULT_MARKET_DATA_DIR, help="Directory for dated JSON snapshots")
    parser.add_argument("--stdout-only", action="store_true", help="Print JSON without writing a snapshot")
    parser.add_argument("--log-level", default="WARNING", choices=("DEBUG", "INFO", "WARNING", "ERROR"))
    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level), format="%(levelname)s %(message)s")
    snapshot = fetch_market_data()
    if not args.stdout_only:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / f"{snapshot['date_gregorian']}.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
