# GAQL Explorer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB.svg)](https://www.python.org)

A CLI toolkit for exploring Google Ads data via GAQL (Google Ads Query Language). Ships with 17 battle-tested query templates, rich terminal output, and a demo mode that works without any credentials.

Built for PPC auditors, media buyers, and anyone who speaks GAQL.

## Features

- **17 query templates** organized by audit category — campaign performance, search terms, keywords, geo, ad copy, quality scores
- **Demo mode** — realistic mock data (no credentials needed) for learning GAQL and testing workflows
- **Rich terminal output** — formatted tables, JSON, or CSV export
- **Live mode** — query real Google Ads accounts via the API
- **Template browser** — search and preview templates by name or category

## Quick Start

### Install

```bash
pip install -e .
```

### Run in Demo Mode

```bash
# Execute a raw GAQL query against demo data
gaql query "SELECT campaign.name, metrics.cost_micros FROM campaign" --demo

# List all query templates
gaql templates --list

# Run a template against demo data
gaql templates campaign_performance_30d --demo

# Preview all templates with demo output
gaql demo
```

### Connect to Real Accounts

```bash
cp .env.example .env
# Fill in your Google Ads API credentials

# List accessible accounts
gaql accounts

# Run a query against a live account
gaql query "SELECT campaign.name, metrics.clicks FROM campaign WHERE segments.date DURING LAST_7_DAYS" -c 123-456-7890

# Run a template and export to CSV
gaql templates wasted_spend_terms -c 123-456-7890 -f csv -o wasted.csv
```

## Template Categories

| Category | Templates | Use Case |
|----------|-----------|----------|
| Campaign Performance | 3 | Spend analysis, budget pacing, bidding strategy review |
| Search Terms | 3 | Wasted spend detection, converting term mining |
| Keywords | 3 | Quality score audit, bid optimization, match type analysis |
| Geographic | 2 | City-level performance, geo exclusion candidates |
| Ad Copy | 3 | RSA performance, headline/description effectiveness |
| Quality & Health | 3 | Low QS keywords, landing page issues, account health |

## Output Formats

```bash
# Rich table (default)
gaql query "..." --demo

# JSON
gaql query "..." --demo -f json

# CSV (great for spreadsheet analysis)
gaql query "..." --demo -f csv -o report.csv
```

## Project Structure

```
src/gaql_explorer/
├── __init__.py       # Package metadata
├── cli.py            # Click CLI commands
├── client.py         # Google Ads API wrapper
├── demo_data.py      # Realistic mock data
├── formatter.py      # Table/JSON/CSV output
└── templates.py      # 17 GAQL query templates
```

## Example Session

```
$ gaql templates wasted_spend_terms --demo

╭─ Template ──────────────────────────────────────────────╮
│ wasted_spend_terms                                      │
│ Search Terms                                            │
│                                                         │
│ Search terms with 10+ clicks and zero conversions       │
│                                                         │
│ When to use: Weekly audit to find negative keyword       │
│ candidates bleeding budget without converting.           │
│                                                         │
│ Query:                                                   │
│ SELECT search_term_view.search_term, ...                 │
╰─────────────────────────────────────────────────────────╯

Results:
┌──────────────────────────────┬────────┬──────────┬─────────────┐
│ Search Term                  │ Clicks │ Cost     │ Conversions │
├──────────────────────────────┼────────┼──────────┼─────────────┤
│ how to mount tv on wall      │     12 │   $45.00 │           0 │
│ tv mount bracket amazon      │      8 │   $30.00 │           0 │
│ tv wall mount diy            │     15 │   $56.00 │           0 │
└──────────────────────────────┴────────┴──────────┴─────────────┘
```

## Author

**Ruslan Danelian** — [premium.ruslandanelian.com](https://premium.ruslandanelian.com)

I run GAQL daily across 8 Google Ads accounts. This tool is a sanitized version of the query toolkit I use for audits, negative keyword mining, and performance reviews.

## License

MIT — see [LICENSE](LICENSE).
