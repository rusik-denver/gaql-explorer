"""Output formatting: Rich tables, JSON, and CSV."""

import csv
import io
import json
from typing import TextIO

from rich.console import Console
from rich.table import Table


def _micros_to_dollars(value: int | float) -> str:
    return f"${value / 1_000_000:,.2f}"


def _format_value(key: str, value) -> str:
    if value is None:
        return "—"
    if "micros" in key:
        return _micros_to_dollars(value)
    if isinstance(value, float):
        if "ctr" in key or "share" in key or "percentage" in key:
            return f"{value:.1%}"
        return f"{value:,.1f}"
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)


def _short_header(field: str) -> str:
    parts = field.rsplit(".", 1)
    return parts[-1] if len(parts) > 1 else field


def print_table(headers: list[str], rows: list[dict], console: Console | None = None):
    console = console or Console()
    if not rows:
        console.print("[yellow]No results[/yellow]")
        return

    table = Table(show_lines=False, padding=(0, 1))
    for h in headers:
        justify = "right" if any(k in h for k in ("metrics.", "micros", "score", "bid")) else "left"
        table.add_column(_short_header(h), justify=justify, no_wrap=True)

    for row in rows:
        table.add_row(*[_format_value(h, row.get(h)) for h in headers])

    console.print(table)


def print_json(headers: list[str], rows: list[dict], file: TextIO | None = None):
    output = []
    for row in rows:
        output.append({_short_header(h): row.get(h) for h in headers})
    text = json.dumps(output, indent=2)
    if file:
        file.write(text)
    else:
        print(text)


def print_csv(headers: list[str], rows: list[dict], file: TextIO | None = None):
    buf = file or io.StringIO()
    short = [_short_header(h) for h in headers]
    writer = csv.DictWriter(buf, fieldnames=short)
    writer.writeheader()
    for row in rows:
        writer.writerow({_short_header(h): row.get(h) for h in headers})
    if file is None:
        print(buf.getvalue())
