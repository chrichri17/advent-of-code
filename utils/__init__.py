from importlib import import_module
from pathlib import Path

base_dir = Path(__file__).parent.parent


def get_last_year() -> str:
    last_year = ""

    for p in base_dir.iterdir():
        if p.is_dir() and p.name.startswith("year"):
            last_year = max(last_year, p.name.split("_")[-1])

    return last_year


def get_last_day(last_year: str) -> str:
    year_dir = base_dir / f"year_{last_year}"
    last_day = 0

    for p in year_dir.iterdir():
        if p.is_dir() and p.name[:2].isdigit():
            last_day = max(last_day, int(p.name[:2]))

    return f"{last_day:02d}"


def get_module(year: str, day: str) -> str:
    year_dir = base_dir / f"year_{year}"

    for p in year_dir.iterdir():
        if p.name.startswith(day):
            return import_module(f"year_{year}.{p.name}.main")
