"""CLI interface: query, templates, accounts, demo commands."""

import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from . import __version__
from .demo_data import resolve_query
from .formatter import print_csv, print_json, print_table
from .templates import TEMPLATES, get_by_category, get_by_name, get_categories

console = Console()


@click.group()
@click.version_option(__version__, prog_name="gaql-explorer")
def cli():
    """GAQL Explorer — Google Ads Query Language toolkit for auditors and analysts."""


@cli.command()
@click.argument("query")
@click.option("--customer-id", "-c", help="Google Ads customer ID (e.g. 123-456-7890)")
@click.option("--format", "-f", "fmt", type=click.Choice(["table", "json", "csv"]), default="table")
@click.option("--demo", is_flag=True, help="Run against built-in demo data instead of the API")
@click.option("--output", "-o", type=click.Path(), help="Write output to file")
def query(query, customer_id, fmt, demo, output):
    """Execute a GAQL query against the API or demo data."""
    if demo:
        headers, rows = resolve_query(query)
    else:
        if not customer_id:
            console.print("[red]Error:[/red] --customer-id required for live queries (or use --demo)")
            sys.exit(1)
        from .client import GoogleAdsClient
        client = GoogleAdsClient()
        if not client.is_configured:
            console.print("[red]Error:[/red] Google Ads API credentials not configured.")
            console.print("Copy .env.example to .env and fill in your credentials.")
            sys.exit(1)
        headers, rows = client.query(customer_id, query)

    if not rows:
        console.print("[yellow]No results returned.[/yellow]")
        return

    file = open(output, "w") if output else None
    try:
        if fmt == "json":
            print_json(headers, rows, file=file)
        elif fmt == "csv":
            print_csv(headers, rows, file=file)
        else:
            print_table(headers, rows, console=console)
    finally:
        if file:
            file.close()
            console.print(f"[green]Wrote {len(rows)} rows to {output}[/green]")


@cli.command()
@click.argument("template_name", required=False)
@click.option("--category", "-g", help="Filter by category")
@click.option("--list", "-l", "list_all", is_flag=True, help="List all templates")
@click.option("--demo", is_flag=True, help="Run the template against demo data")
@click.option("--customer-id", "-c", help="Customer ID for live execution")
@click.option("--format", "-f", "fmt", type=click.Choice(["table", "json", "csv"]), default="table")
def templates(template_name, category, list_all, demo, customer_id, fmt):
    """Browse and run GAQL query templates."""
    if list_all or (not template_name and not category):
        for cat in get_categories():
            console.print(f"\n[bold cyan]{cat}[/bold cyan]")
            for t in get_by_category(cat):
                console.print(f"  [green]{t.name}[/green] — {t.description}")
        return

    if category:
        results = get_by_category(category)
        if not results:
            console.print(f"[red]No templates in category '{category}'[/red]")
            console.print(f"Available: {', '.join(get_categories())}")
            return
        for t in results:
            console.print(f"  [green]{t.name}[/green] — {t.description}")
        return

    template = get_by_name(template_name)
    if not template:
        console.print(f"[red]Template '{template_name}' not found.[/red]")
        close_matches = [t.name for t in TEMPLATES if template_name.lower() in t.name.lower()]
        if close_matches:
            console.print(f"Did you mean: {', '.join(close_matches)}?")
        return

    console.print(Panel.fit(
        Text.from_markup(
            f"[bold]{template.name}[/bold]\n"
            f"[dim]{template.category}[/dim]\n\n"
            f"{template.description}\n\n"
            f"[bold]When to use:[/bold] {template.when_to_use}\n\n"
            f"[bold]Query:[/bold]\n[cyan]{template.query}[/cyan]"
        ),
        title="Template",
    ))

    if demo or customer_id:
        console.print("\n[bold]Results:[/bold]")
        if demo:
            headers, rows = resolve_query(template.query)
        else:
            from .client import GoogleAdsClient
            client = GoogleAdsClient()
            headers, rows = client.query(customer_id, template.query)

        if fmt == "json":
            print_json(headers, rows)
        elif fmt == "csv":
            print_csv(headers, rows)
        else:
            print_table(headers, rows, console=console)


@cli.command()
def accounts():
    """List accessible Google Ads accounts."""
    from .client import GoogleAdsClient
    client = GoogleAdsClient()
    if not client.is_configured:
        console.print("[red]Error:[/red] API credentials not configured.")
        console.print("Copy .env.example to .env and fill in your credentials.")
        sys.exit(1)

    accts = client.list_accounts()
    for a in accts:
        console.print(f"  [green]{a['id']}[/green]  {a['name']}")


@cli.command()
@click.option("--format", "-f", "fmt", type=click.Choice(["table", "json", "csv"]), default="table")
def demo(fmt):
    """Run all templates against demo data to preview output."""
    for template in TEMPLATES[:5]:
        console.print(f"\n[bold cyan]▸ {template.name}[/bold cyan] — {template.description}")
        headers, rows = resolve_query(template.query)
        if fmt == "json":
            print_json(headers, rows)
        elif fmt == "csv":
            print_csv(headers, rows)
        else:
            print_table(headers, rows, console=console)


if __name__ == "__main__":
    cli()
