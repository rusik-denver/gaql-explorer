# GAQL Explorer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB.svg)](https://www.python.org)

A CLI toolkit and web UI for exploring Google Ads data via GAQL (Google Ads Query Language). Ships with 17 battle-tested query templates, rich terminal output, and a demo mode that works without any credentials.

Built for PPC auditors, media buyers, and anyone who speaks GAQL.

## Features

- **17 query templates** organized by audit category — campaign performance, search terms, keywords, geo, ad copy, quality scores, negatives
- **Demo mode** — realistic mock data (no credentials needed) for learning GAQL and testing workflows
- **Rich terminal output** — formatted tables, JSON, or CSV export
- **Web UI** — browser-based query explorer with template cards and live results
- **Live mode** — query real Google Ads accounts via the API
- **Template browser** — search and preview templates by name or category

## Quick Start

### Install

```bash
pip install gaql-explorer

# With web UI
pip install 'gaql-explorer[web]'

# With live API support
pip install 'gaql-explorer[api]'

# Everything
pip install 'gaql-explorer[api,web]'
```

### Run in Demo Mode

```bash
# Execute a raw GAQL query against demo data
gaql query "SELECT campaign.name, metrics.cost_micros FROM campaign ORDER BY metrics.cost_micros DESC" --demo

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
gaql templates wasted_search_terms -c 123-456-7890 -f csv -o wasted.csv
```

### Web UI

```bash
pip install 'gaql-explorer[web]'
python -m gaql_explorer.web
# Open http://127.0.0.1:5000
```

Click any template card to load and run its query, or write your own GAQL in the editor.

## Template Categories

| Category | Count | Use Case |
|----------|-------|----------|
| Campaign Performance | 4 | Spend analysis, conversions, device splits, hourly patterns |
| Budget Utilization | 1 | Budget vs. spend, impression share gaps |
| Search Term Analysis | 3 | Wasted spend detection, converting term mining, match leakage |
| Quality Score | 1 | QS components by keyword for optimization |
| Keyword Metrics | 2 | Bid landscape, low-impression keyword cleanup |
| Geographic Performance | 2 | City-level performance, geo exclusion candidates |
| Ad Copy Performance | 2 | RSA asset ratings, landing page metrics |
| Negative Keyword Audit | 2 | Campaign negatives, shared list coverage |

## Output Formats

```bash
# Rich table (default)
gaql query "..." --demo

# JSON
gaql query "..." --demo -f json

# CSV (great for spreadsheet analysis)
gaql query "..." --demo -f csv -o report.csv
```

## As a Library

```python
from gaql_explorer.templates import TEMPLATES, get_by_name
from gaql_explorer.demo_data import resolve_query
from gaql_explorer.formatter import print_table

# Run a template against demo data
template = get_by_name("wasted_search_terms")
headers, rows = resolve_query(template.query)
print_table(headers, rows)

# Live API
from gaql_explorer.client import GoogleAdsClient
client = GoogleAdsClient()
headers, rows = client.query("1234567890", template.query)
```

## Project Structure

```
src/gaql_explorer/
  __init__.py       # Package metadata
  cli.py            # Click CLI commands
  client.py         # Google Ads API wrapper
  demo_data.py      # Realistic mock dataset
  formatter.py      # Table/JSON/CSV output
  templates.py      # 17 GAQL query templates
  web.py            # Flask web UI
```

## Author

**Ruslan Danelian** — [premium.ruslandanelian.com](https://premium.ruslandanelian.com)

I run GAQL daily across 8 Google Ads accounts. This tool is a sanitized version of the query toolkit I use for audits, negative keyword mining, and performance reviews.

## License

MIT — see [LICENSE](LICENSE).
