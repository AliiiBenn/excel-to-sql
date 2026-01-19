# Excel to SQLite CLI

<div align="center">

**A powerful command-line interface tool for importing Excel files into SQLite databases and exporting back with intelligent formatting.**

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/davidfrancoeur/excel-to-sql)

[Features](#-features) •
[Installation](#-installation) •
[Quick Start](#-quick-start) •
[Documentation](#-documentation) •
[Examples](#-examples)

</div>

---

## ✨ Features

### 📥 Import Excel to SQLite
- **Automatic schema detection** - Creates tables from Excel data
- **Column mapping** - Flexible mapping configuration with type conversion
- **Composite primary keys** - Support for multi-column primary keys
- **Change detection** - SHA256 content hashing prevents duplicate imports
- **UPSERT logic** - Intelligently updates existing rows and inserts new ones
- **Data cleaning** - Automatic whitespace trimming and empty row removal

### 📤 Export SQLite to Excel
- **Table export** - Export entire tables to Excel
- **Custom queries** - Export results of SQL SELECT queries
- **Excel formatting** - Bold headers, auto-width columns, frozen header row
- **Export history** - Track all exports in the database

### 📊 Status & Monitoring
- **Import history** - View all imports with timestamps
- **Statistics** - Total imports, rows, success rate
- **Rich display** - Beautiful terminal output with colors and tables

### 🎯 Key Capabilities
- ⚡ **Fast** - Powered by Pandas and SQLAlchemy 2.0
- 🔒 **Reliable** - ACID-compliant SQLite transactions
- 🎨 **Beautiful CLI** - Rich terminal interface with colored output
- 📝 **Type-safe** - Full type hints and Pydantic validation
- 🧪 **Well-tested** - Comprehensive test suite

---

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Install from source

```bash
# Clone the repository
git clone https://github.com/davidfrancoeur/excel-to-sql.git
cd excel-to-sql

# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

### Development installation

```bash
# Install with dev dependencies
uv sync --dev

# Or with pip
pip install -e ".[dev]"
```

---

## 🚀 Quick Start

### 1. Initialize a project

```bash
excel-to-sql init
```

This creates the project structure:
```
.
├── .git/                    # Git repository
├── config/                  # Configuration files
│   └── mappings.json        # Column mappings
├── data/                    # Database directory
│   └── warehouse.db         # SQLite database
├── imports/                 # Excel files to import
├── exports/                 # Exported Excel files
└── logs/                    # Log files
```

### 2. Configure a mapping

Edit `config/mappings.json` to define your data types:

```json
{
  "products": {
    "target_table": "products",
    "primary_key": ["id"],
    "column_mappings": {
      "ID": {"target": "id", "type": "integer", "required": true},
      "Name": {"target": "name", "type": "string"},
      "Price": {"target": "price", "type": "float"},
      "Created": {"target": "created_at", "type": "date"}
    }
  }
}
```

### 3. Import data

```bash
# Import an Excel file
excel-to-sql import --file imports/products.xlsx --type products

# Force re-import even if file hasn't changed
excel-to-sql import --file imports/products.xlsx --type products --force
```

### 4. Check status

```bash
excel-to-sql status
```

### 5. Export data

```bash
# Export entire table
excel-to-sql export --table products --output exports/products.xlsx

# Export with custom query
excel-to-sql export --query "SELECT * FROM products WHERE price > 100" --output expensive.xlsx
```

---

## 📚 Documentation

### Commands Reference

#### `init` - Initialize project

```bash
excel-to-sql init [--db-path PATH]
```

**Options:**
- `--db-path`: Custom database path (default: `data/warehouse.db`)

**What it does:**
- Creates project directory structure
- Initializes SQLite database
- Creates configuration file with example mapping

---

#### `import` - Import Excel to SQLite

```bash
excel-to-sql import --file FILE --type TYPE [--force]
```

**Required options:**
- `--file`, `-f`: Path to Excel file (.xlsx)
- `--type`, `-t`: Mapping type name (from `config/mappings.json`)

**Optional options:**
- `--force`: Re-import even if file hasn't changed

**Features:**
- ✅ Detects file changes via SHA256 hash
- ✅ Cleans data (removes empty rows, trims whitespace)
- ✅ Applies column mappings and type conversions
- ✅ Performs UPSERT (insert/update)
- ✅ Records import history
- ✅ Shows summary table

**Supported column types:**
- `integer` - Whole numbers
- `float` - Decimal numbers
- `string` - Text
- `boolean` - TRUE/FALSE values
- `date` - Date/datetime values

---

#### `status` - Show import history

```bash
excel-to-sql status
```

**Displays:**
- 📊 Import history table (Date, File, Type, Rows, Status)
- 📈 Statistics:
  - Total imports
  - Total rows imported
  - Total rows skipped
  - Success rate
  - Last import timestamp

---

#### `export` - Export SQLite to Excel

```bash
excel-to-sql export --output OUTPUT [--table TABLE] [--query QUERY]
```

**Required options:**
- `--output`, `-o`: Output Excel file path

**Exclusive options** (one required):
- `--table`: Export entire table
- `--query`: Custom SQL SELECT query

**Features:**
- ✅ Excel formatting:
  - Bold headers
  - Auto-adjusted column widths
  - Frozen header row
- ✅ Export history tracking
- ✅ Summary table with file size
- ✅ Automatic output directory creation

**Examples:**
```bash
# Export table
excel-to-sql export --table products --output report.xlsx

# Export with query
excel-to-sql export --query "SELECT * FROM products WHERE price > 50" --output expensive.xlsx

# Export with joins
excel-to-sql export --query "
  SELECT p.name, c.name as category
  FROM products p
  LEFT JOIN categories c ON p.category_id = c.id
" --output products_with_categories.xlsx
```

---

#### `config` - Manage configurations (Coming Soon)

```bash
excel-to-sql config --add-type TYPE --table TABLE --pk PK
excel-to-sql config --list
excel-to-sql config --show TYPE
excel-to-sql config --remove TYPE
```

**Status:** ⚙️ Planned for v0.2.0

---

## 💡 Examples

### Example 1: Import products with composite primary key

**Excel file** (`products.xlsx`):
| Product ID | Region | Name | Price |
|------------|--------|------|-------|
| 1 | US | Widget A | 10.50 |
| 1 | EU | Widget A | 12.00 |
| 2 | US | Widget B | 20.00 |

**Mapping** (`config/mappings.json`):
```json
{
  "product_pricing": {
    "target_table": "product_pricing",
    "primary_key": ["product_id", "region"],
    "column_mappings": {
      "Product ID": {"target": "product_id", "type": "integer"},
      "Region": {"target": "region", "type": "string"},
      "Name": {"target": "name", "type": "string"},
      "Price": {"target": "price", "type": "float"}
    }
  }
}
```

**Import:**
```bash
excel-to-sql import --file products.xlsx --type product_pricing
```

---

### Example 2: Import and export workflow

```bash
# 1. Initialize project
excel-to-sql init

# 2. Configure mapping (edit config/mappings.json)
# 3. Import data
excel-to-sql import --file sales.xlsx --type sales

# 4. Check what was imported
excel-to-sql status

# 5. Query and export specific data
excel-to-sql export --query "
  SELECT
    date,
    product_name,
    quantity,
    revenue
  FROM sales
  WHERE revenue > 1000
  ORDER BY revenue DESC
" --output top_sales.xlsx

# 6. Import new data (updates existing, adds new)
excel-to-sql import --file sales_updated.xlsx --type sales

# 7. Check final status
excel-to-sql status
```

---

### Example 3: Multiple file types in one project

```bash
# Import products
excel-to-sql import --file products.xlsx --type products

# Import orders
excel-to-sql import --file orders.xlsx --type orders

# Import customers
excel-to-sql import --file customers.xlsx --type customers

# View all imports
excel-to-sql status
```

**Output:**
```
╭─────────────────────────────────────────────────────────────╮
│                      Import History                          │
├────────────────┬────────────────┬──────────┬──────┬────────┤
│ Date           │ File           │ Type     │ Rows │ Status │
├────────────────┼────────────────┼──────────┼──────┼────────┤
│ 2026-01-19     │ products.xlsx  │ products │ 150  │ success│
│ 2026-01-19     │ orders.xlsx    │ orders   │ 500  │ success│
│ 2026-01-19     │ customers.xlsx │ customers│ 75   │ success│
╰────────────────┴────────────────┴──────────┴──────┴────────╯

Statistics:
  Total imports: 3
  Total rows: 725
  Total skipped: 0
  Success rate: 100.0%
  Last import: 2026-01-19 14:30:00
```

---

## 📁 Project Structure

```
excel-to-sql/
├── excel_to_sql/              # Main package
│   ├── __init__.py
│   ├── __main__.py           # Entry point
│   ├── cli.py                # CLI interface
│   ├── entities/             # Business entities
│   │   ├── project.py        # Project management
│   │   ├── database.py       # Database operations
│   │   ├── excel_file.py     # Excel file handling
│   │   ├── dataframe.py      # Data processing
│   │   └── table.py          # Table operations
│   ├── models/               # Pydantic models
│   │   └── mapping.py        # Mapping validation
│   └── config/               # Configuration (user)
├── tests/                    # Test suite
│   ├── test_import.py        # Import tests
│   ├── test_export.py        # Export tests
│   ├── test_status.py        # Status tests
│   └── ...
├── docs/                     # Documentation
│   ├── ANALYSIS.md           # Codebase analysis
│   ├── ARCHITECTURE.md       # Technical architecture
│   ├── ROADMAP.md            # Development roadmap
│   └── SPECIFICATIONS.md     # Functional specifications
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

---

## 🏗️ Architecture

The project follows an **entity-oriented architecture** with clear separation of concerns:

```
┌─────────────────────────────────────┐
│            CLI (Typer)              │  ← User interface
├─────────────────────────────────────┤
│         Entities (Business)         │  ← Business logic
│  ┌─────────┐ ┌─────────┐           │
│  │ Project │ │ Database│           │
│  └─────────┘ └─────────┘           │
│  ┌─────────┐ ┌─────────┐           │
│  │ExcelFile│ │DataFrame│           │
│  └─────────┘ └─────────┘           │
│  ┌─────────┐                       │
│  │  Table  │                       │
│  └─────────┘                       │
├─────────────────────────────────────┤
│        Models (Pydantic)            │  ← Validation
└─────────────────────────────────────┘
```

**Key design decisions:**
- **No foreign keys** - Implicit relationships for flexibility
- **SQLite** - Simple, portable, serverless database
- **UPSERT** - Update existing, insert new automatically
- **Content hashing** - Detect file changes efficiently
- **Entity-oriented** - Modular, testable code

For detailed architecture, see [ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## 🧪 Testing

### Run tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=excel_to_sql

# Run specific test file
uv run pytest tests/test_import.py

# Run with verbose output
uv run pytest -v
```

**Test coverage:**
- ✅ 112 tests passing
- ✅ Import/export/status commands
- ✅ All entities tested
- ✅ Edge cases covered

---

## 🗺️ Roadmap

### ✅ Completed (v0.1.0)
- [x] `init` command - Project initialization
- [x] `import` command - Excel to SQLite
- [x] `status` command - Import history
- [x] `export` command - SQLite to Excel
- [x] Composite primary key support
- [x] Export history tracking

### 🚧 In Progress (v0.2.0)
- [ ] `config` command - Configuration management
  - [ ] `--add-type` with auto-detection
  - [ ] `--list` all mappings
  - [ ] `--show <type>` details
  - [ ] `--remove <type>`
  - [ ] `--validate` mappings

### 📋 Planned (v0.3.0)
- [ ] Pre-import data validation
- [ ] Progress bars for long operations
- [ ] Custom transformations
- [ ] Multiple sheet support
- [ ] Enhanced Excel formatting

### 💭 Future (v1.0.0)
- [ ] PostgreSQL/MySQL support
- [ ] Performance optimizations
- [ ] Advanced query features
- [ ] GUI interface

For details, see [ROADMAP.md](docs/ROADMAP.md).

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development setup

```bash
# Fork the repository
git clone https://github.com/YOUR_USERNAME/excel-to-sql.git
cd excel-to-sql

# Install development dependencies
uv sync --dev

# Run tests
uv run pytest

# Make your changes and commit
git commit -m "feat: add new feature"
```

### Commit convention

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**David Francoeur**

- GitHub: [@davidfrancoeur](https://github.com/davidfrancoeur)

---

## 🙏 Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) - CLI framework
- Data processing with [Pandas](https://pandas.pydata.org/)
- Excel I/O with [openpyxl](https://openpyxl.readthedocs.io/)
- Database with [SQLAlchemy](https://www.sqlalchemy.org/)
- Beautiful output with [Rich](https://rich.readthedocs.io/)
- Validation with [Pydantic](https://docs.pydantic.dev/)

---

## 📞 Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/davidfrancoeur/excel-to-sql/issues)
- 💬 [Discussions](https://github.com/davidfrancoeur/excel-to-sql/discussions)

---

<div align="center">

**Made with ❤️ by David Francoeur**

[⬆ Back to top](#excel-to-sqlite-cli)

</div>
