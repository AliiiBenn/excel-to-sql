# Excel to SQLite

> A powerful CLI tool and Python SDK for importing Excel files into SQLite databases with advanced data transformation, validation, and quality profiling.

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/excel-to-sql)](https://pypi.org/project/excel-to-sql/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## ✨ Features

### Core Functionality
- 📥 **Smart Import** - Import Excel files into SQLite with automatic schema detection
- 📤 **Flexible Export** - Export SQL data back to Excel with formatting
- 🔁 **Incremental Imports** - Only process changed files using content hashing
- 📑 **Multi-Sheet Support** - Import/export multiple sheets in one operation
- ⚡ **High Performance** - Powered by Pandas and SQLAlchemy 2.0
- 🔄 **UPSERT Logic** - Automatically insert new rows or update existing ones
- 🧹 **Data Cleaning** - Automatic whitespace trimming and empty row removal
- 📊 **Rich Terminal Display** - Beautiful colored output with tables and progress

### Data Transformations
- 🔄 **Value Mapping** - Standardize data values (e.g., "NY" → "New York")
- ➕ **Calculated Columns** - Create derived columns using expressions
- 🔗 **Reference Validation** - Foreign key validation against lookup tables
- 🎣 **Pre/Post Hooks** - Execute custom code during import/export pipeline

### Data Validation
- ✅ **Custom Validators** - Range, regex, unique, not-null, enum validators
- 📏 **Validation Rules** - Declarative rule-based validation system
- 🔍 **Data Profiling** - Automatic quality analysis with detailed reports
- 🏷️ **Metadata Tracking** - Tag and categorize imports with rich metadata

### Developer Experience
- 🐍 **Python SDK** - Full-featured programmatic API
- 🎯 **Type Hints** - Complete type annotations throughout
- 📚 **Well Documented** - Comprehensive documentation and examples
- 🧪 **Well Tested** - Extensive test coverage

## 📦 Installation

```bash
# Install from PyPI
pip install excel-to-sql

# Or with uv
uv pip install excel-to-sql

# Or install from source
git clone https://github.com/wareflowx/excel-to-sql.git
cd excel-to-sql
uv sync
```

## 🚀 Quick Start

### CLI Usage

```bash
# Initialize a new project
excel-to-sql init

# Define a mapping type (interactive)
excel-to-sql config add --type products

# Import an Excel file
excel-to-sql import --file data.xlsx --type products

# Check import status
excel-to-sql status

# Export to Excel
excel-to-sql export --table products --output report.xlsx

# Profile data quality
excel-to-sql profile --table products --output quality-report.html
```

### Python SDK

```python
from excel_to_sql import ExcelToSqlite

# Initialize SDK
sdk = ExcelToSqlite()

# Import data with transformations
result = sdk.import_excel(
    file_path="data.xlsx",
    type_name="products",
    tags=["q1-2024", "verified"]
)

# Query data
df = sdk.query("SELECT * FROM products WHERE price > 100")

# Profile data
profile = sdk.profile_table("products")
print(f"Quality score: {profile['summary']['null_percentage']}% nulls")

# Export with multi-sheet support
sdk.export_to_excel(
    output="report.xlsx",
    sheet_mapping={
        "Products": "products",
        "Categories": "SELECT * FROM categories"
    }
)
```

### Advanced Transformations

```python
from excel_to_sql import ExcelToSqlite, ValueMapping, CalculatedColumn
from excel_to_sql.validators import ValidationRule, RuleSet

sdk = ExcelToSqlite()

# Configure value mappings
value_mappings = {
    "status": {"1": "Active", "0": "Inactive"},
    "state": {"NY": "New York", "CA": "California"}
}

# Configure calculated columns
calculated_columns = [
    CalculatedColumn("total", "quantity * price"),
    CalculatedColumn("tax", "total * 0.1"),
    CalculatedColumn("grand_total", "total + tax")
]

# Configure validation rules
validation_rules = [
    ValidationRule("id", "unique"),
    ValidationRule("email", "regex", {"pattern": r"^[^@]+@[^@]+\.[^@]+$"}),
    ValidationRule("age", "range", {"min": 0, "max": 120})
]
```

### Data Quality Reports

```python
from excel_to_sql import QualityReport

# Generate quality report
report = QualityReport()
profile = report.generate(
    df=df,
    output_path="quality-report.html"
)

# Access quality metrics
print(f"Null percentage: {profile.null_percentage}%")
print(f"Unique values: {profile.unique_count}")
print(f"Issues found: {len(profile.get_issues())}")
```

### Core Features (Original v0.1.x)

#### Automatic Schema Detection

Tables are automatically created from Excel data with appropriate types:

```bash
excel-to-sql import --file products.xlsx --type products

# Output:
# ✓ Table 'products' created automatically
# ✓ Detected columns: id (integer), name (string), price (float)
# ✓ Imported 150 rows
```

#### Column Mapping Configuration

Define how Excel columns map to database columns:

```json
{
  "products": {
    "target_table": "products",
    "primary_key": ["id"],
    "column_mappings": {
      "Product ID": {"target": "id", "type": "integer"},
      "Product Name": {"target": "name", "type": "string"},
      "Unit Price": {"target": "price", "type": "float"},
      "In Stock": {"target": "in_stock", "type": "boolean"},
      "Created Date": {"target": "created_at", "type": "date"}
    }
  }
}
```

#### Type Conversions

Automatic type conversion with support for 5 data types:

```python
from excel_to_sql.entities import DataFrame

# Type conversions happen automatically during import
df = DataFrame(raw_df)
df.apply_mapping(mapping)

# Supported types:
# - string: TEXT columns
# - integer: INTEGER with Int64 (nullable)
# - float: REAL columns
# - boolean: BOOLEAN (0/1)
# - date: TIMESTAMP (ISO-8601)
```

#### UPSERT Logic

Intelligent insert-or-update based on primary keys:

```bash
# First import - inserts 100 rows
excel-to-sql import --file products.xlsx --type products

# Second import with updates:
# - Updates 20 existing rows (based on ID)
# - Inserts 10 new rows
# - Skips unchanged rows
excel-to-sql import --file products_updated.xlsx --type products
```

#### Data Cleaning

Automatic data cleaning during import:

```python
from excel_to_sql.entities import DataFrame

df = DataFrame(raw_df)
df.clean()

# Automatically:
# ✓ Strips whitespace from strings
# ✓ Removes empty strings
# ✓ Drops completely empty rows
# ✓ Lowercases column names
```

#### Rich Terminal Display

Beautiful terminal output with colors and tables:

```bash
$ excel-to-sql import --file data.xlsx --type sales

╭──────────────────────────────────────────────────────────╮
│  Importing Excel file to SQLite                          │
╰──────────────────────────────────────────────────────────╯

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  File: data.xlsx                                        ┃
┃  Type: sales                                            ┃
┃  Rows: 1,234                                            ┃
┃  Columns: 12                                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

⠙ Processing...
✓ Data cleaned
✓ Transformations applied
✓ Data validated (0 errors, 3 warnings)
✓ Data imported to table 'sales'
✓ Import history recorded

╭──────────────────────────────────────────────────────────╮
│  Import completed successfully!                          │
╰──────────────────────────────────────────────────────────╯
```

#### Import History

Track all imports with automatic history:

```bash
$ excel-to-sql history

┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ File      ┃ Type            ┃ Table    ┃ Rows  ┃ Timestamp          ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ data.xlsx │ sales           │ sales    │ 1,234 │ 2024-01-20 10:30   │
│ prod.xlsx │ products        │ products │ 150   │ 2024-01-20 09:15   │
│ cat.xlsx  │ categories      │ categories│ 25    │ 2024-01-20 09:00   │
└───────────┴─────────────────┴──────────┴───────┴────────────────────┘
```

#### Project Management

Initialize and manage projects:

```bash
# Initialize a new project
excel-to-sql init

# Add a new mapping type
excel-to-sql config add --type customers

# List all types
excel-to-sql config list

# Show mapping for a type
excel-to-sql config show --type products

# Remove a type
excel-to-sql config remove --type old_type
```

## 📖 Configuration

Mapping configuration is stored in `config/mappings.json`:

```json
{
  "products": {
    "target_table": "products",
    "primary_key": ["id"],
    "column_mappings": {
      "ID": {"target": "id", "type": "integer"},
      "Name": {"target": "name", "type": "string"},
      "Price": {"target": "price", "type": "float"}
    },
    "value_mappings": [
      {
        "column": "status",
        "mappings": {"1": "Active", "0": "Inactive"}
      }
    ],
    "calculated_columns": [
      {
        "name": "total",
        "expression": "quantity * price"
      }
    ],
    "validation_rules": [
      {
        "column": "id",
        "type": "unique"
      }
    ],
    "tags": ["import", "products"]
  }
}
```

## 🔧 Available Validators

| Validator | Description | Example |
|-----------|-------------|---------|
| `RangeValidator` | Numeric range validation | Age between 0-120 |
| `RegexValidator` | Pattern matching | Email validation |
| `UniqueValidator` | Uniqueness check | Primary keys |
| `NotNullValidator` | Required fields | Mandatory columns |
| `EnumValidator` | Allowed values | Status codes |
| `ReferenceValidator` | Foreign key check | Category exists |
| `CustomValidator` | Custom logic | Any Python function |

## 📊 Data Profiling

Generate comprehensive data quality reports:

```python
from excel_to_sql import DataProfiler

profiler = DataProfiler()
profile = profiler.profile(df)

# Check for issues
for issue in profile.get_issues():
    print(f"{issue['severity']}: {issue['issue']} in {issue['column']}")
```

Supported report formats:
- **JSON** - Machine-readable format
- **Markdown** - Human-readable documentation
- **HTML** - Interactive reports with styling

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=excel_to_sql --cov-report=html

# Run specific test file
uv run pytest tests/test_transformations.py -v
```

## 📝 Project Structure

```
excel-to-sqlite/
├── excel_to_sql/          # Main package
│   ├── cli.py            # CLI interface
│   ├── sdk/              # Python SDK
│   ├── entities/         # Domain entities
│   ├── transformations/  # Data transformations
│   ├── validators/       # Data validation
│   ├── profiling/        # Quality analysis
│   ├── metadata/         # Metadata management
│   └── models/           # Pydantic models
├── tests/                # Test suite
├── docs/                 # Documentation
└── config/               # Configuration files
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Documentation](docs/)
- [Changelog](CHANGELOG.md)
- [Issue Tracker](https://github.com/wareflowx/excel-to-sql/issues)
- [PyPI Package](https://pypi.org/project/excel-to-sql/)

## 🎉 Version 0.2.0 Highlights

**12 Major Features Added:**
1. ✅ Value Mapping for Data Standardization
2. ✅ Calculated/Derived Columns
3. ✅ Custom Validators
4. ✅ Reference/Lookup Validation
5. ✅ Data Profiling & Quality Reports
6. ✅ Multi-Sheet Import
7. ✅ Multi-Sheet Export
8. ✅ Incremental/Delta Import
9. ✅ Data Validation Rules
10. ✅ Pre/Post Processing Hooks
11. ✅ Python SDK / Programmatic API
12. ✅ Metadata & Tags for Imports

**68 tests added** with comprehensive coverage for all new features.
