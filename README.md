# Excel to SQL CLI

A command-line interface tool for importing Excel files into SQL databases and exporting back with intelligent formatting.

## Features

- 📥 **Import** Excel files into SQL with automatic schema detection
- 📤 **Export** SQL data to Excel with formatting options
- 🔁 **Incremental imports** - only process changed files
- 🗃️ **Implicit foreign keys** - flexible joins without strict constraints
- ⚡ **Fast** - powered by Pandas and SQLAlchemy
- 🎯 **Entity-oriented** - clean, Pythonic API

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd excel-to-sql

# Install with uv
uv sync

# Or with pip
pip install -e .
```

## Quick Start

```bash
# Initialize project
excel-to-sql init

# Import an Excel file
excel-to-sql import --file data.xlsx --type orders

# Check import status
excel-to-sql status

# Export to Excel
excel-to-sql export --table orders --output report.xlsx
```

## Documentation

See [docs/](docs/) for detailed documentation:
- [PROJECT.md](docs/PROJECT.md) - Full project documentation
- [MVP.md](docs/MVP.md) - Minimum Viable Product scope

## License

MIT
