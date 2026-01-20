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
git clone https://github.com/AliiiBenn/excel-to-sql.git
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
- [Issue Tracker](https://github.com/AliiiBenn/excel-to-sql/issues)
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
