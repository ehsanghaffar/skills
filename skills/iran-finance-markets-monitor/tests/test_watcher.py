import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "iran_market_watcher.py"
SPEC = importlib.util.spec_from_file_location("iran_market_watcher", SCRIPT)
WATCHER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(WATCHER)


def test_normalize_and_parse_localized_number():
    assert WATCHER.normalize_digits("۱۲۳٬۴۵۶٫۷۸") == "123,456.78"
    assert WATCHER.parse_number("۱۲۳٬۴۵۶ تومان") == 123456
    assert WATCHER.parse_number("-") is None


def test_rial_to_toman_conversion():
    assert WATCHER.rial_to_toman("۲٬۰۰۰٬۰۰۰ ریال") == 200000
    assert WATCHER.rial_to_toman("نامشخص") is None


def test_range_gate_rejects_implausible_values():
    assert WATCHER.validate_range("usd_free", 250000) == (True, "ok")
    valid, reason = WATCHER.validate_range("usd_free", 10)
    assert not valid
    assert "outside" in reason


def test_exact_table_row_matching_avoids_keyword_collisions():
    class Cell:
        def __init__(self, text):
            self.text = text

        def get_text(self, *_args, **_kwargs):
            return self.text

    class Row:
        def __init__(self, cells):
            self.cells = [Cell(cell) for cell in cells]

        def find_all(self, tags):
            return self.cells

    class Table:
        def find_all(self, tag):
            return [Row(["دلار نیما", "1"]), Row(["دلار", "2"])]

    assert WATCHER.parse_table_row(Table(), ["دلار"]) == ["دلار", "2"]