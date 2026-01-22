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
- 🤖 **Auto-Pilot Mode** - Zero-configuration automatic setup with pattern detection
- 🎯 **Interactive Wizard** - Step-by-step guided configuration

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

## 🤖 Auto-Pilot Mode

The Auto-Pilot mode provides **zero-configuration** Excel to SQLite import with automatic pattern detection, quality scoring, and intelligent recommendations. No manual configuration required!

### Quick Start with Auto-Pilot

```bash
# Automatic mode - analyze and generate configuration
excel-to-sql magic --data ./excels

# Interactive mode - guided step-by-step setup
excel-to-sql magic --data ./excels --interactive

# Dry run - analyze without generating configuration
excel-to-sql magic --data ./excels --dry-run
```

### What Auto-Pilot Detects

**Pattern Detection:**
- 📌 Primary Keys - Automatically identifies unique columns
- 🔗 Foreign Keys - Detects relationships between tables
- 🔄 Value Mappings - Finds code columns (e.g., "1"/"0" → "Active"/"Inactive")
- 📊 Split Fields - Identifies redundant status columns to combine
- 🎯 Data Types - Infers SQL types from data

**Quality Analysis:**
- 📈 Quality Score (0-100) with letter grades (A-D)
- ⚠️ Issue Detection (null values, duplicates, type mismatches)
- 📊 Statistical Analysis (value distributions, outliers)
- 🔍 Data Profiling (column types, null percentages)

**Smart Recommendations:**
- 💡 Prioritized suggestions (HIGH/MEDIUM/LOW)
- 🛠️ Auto-Fixable issues with one-click corrections
- 📝 Default value suggestions
- 🌐 French code detection (ENTRÉE→inbound, SORTIE→outbound, etc.)

### Automatic Mode Example

```bash
$ excel-to-sql magic --data ./excels --output .excel-to-sql

╭──────────────────────────────────────────────────────────╮
│              AUTO-PILOT MODE                             │
│  Intelligent Excel to SQLite Configuration              │
╰──────────────────────────────────────────────────────────╯

Found 3 Excel file(s) in ./excels

⠙ Analyzing Excel files...
✓ Analyzed commandes.xlsx (20 rows, 5 columns)
✓ Analyzed mouvements.xlsx (50 rows, 7 columns)
✓ Analyzed produits.xlsx (10 rows, 4 columns)

╭──────────────────────────────────────────────────────────╮
│              DETECTION SUMMARY                           │
│          3 table(s) analyzed                             │
╰──────────────────────────────────────────────────────────╯

┏━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━┳━━━━━━━━┓
┃ Table    ┃ Rows  ┃ Primary Key ┃ Value    ┃ FKs ┃ Score  ┃
┃          ┃       ┃             ┃ Maps     ┃     ┃        ┃
┡━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━╇━━━━━━━━┩
│ commandes│ 20    │ id          │ OK       │ 1   │ 92%    │
│ mouvements│ 50   │ id          │ OK       │ 2   │ 88%    │
│ produits │ 10    │ id          │ OK       │ 0   │ 95%    │
└──────────┴───────┴─────────────┴──────────┴─────┴────────┘

✓ Configuration generated successfully!
  Location: .excel-to-sql/mappings.json
  Tables: 3
  Total Rows: 80
```

### Interactive Mode Example

```bash
$ excel-to-sql magic --data ./excels --interactive

╭──────────────────────────────────────────────────────────╮
│          INTERACTIVE IMPORT MODE                         │
│       Guided setup with explanations                      │
╰──────────────────────────────────────────────────────────╯

You will be guided step-by-step through the configuration
process for each Excel file.

For each file, you can:
  [bold green]1[/bold green] Accept all transformations
  [bold yellow]3[/bold yellow] Skip this file
  [bold cyan]4[/bold cyan] View sample data (10 rows)
  [bold blue]5[/bold blue] View statistics

Press ENTER to begin...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 1/3: commandes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                   File Analysis                        ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Metric          │ Value                                │
├─────────────────┼──────────────────────────────────────┤
│ Rows            │ 20                                   │
│ Columns         │ 5                                    │
│ Primary Key     │ id                                   │
│ Quality Score   │ 92/100 (A)                           │
│ Transformations │ 2                                    │
└─────────────────┴──────────────────────────────────────┘

Detected Transformations:

  1. Value Mapping: type
     ENTRÉE -> inbound
     SORTIE -> outbound

  2. Calculated Column: status
     Expression: COALESCE(etat_superieur, etat_inferieur)

Choice [1/3/4/5/h] (or 'q' to cancel): 1
✓ All transformations accepted
```

### Auto-Pilot Components

**PatternDetector** - Analyzes Excel files and detects patterns:
```python
from excel_to_sql.auto_pilot import PatternDetector

detector = PatternDetector()
patterns = detector.detect_patterns(df, "table_name")

# Returns:
# {
#     "primary_key": "id",
#     "foreign_keys": [...],
#     "value_mappings": {...},
#     "split_fields": [...],
#     "confidence": 0.92
# }
```

**QualityScorer** - Generates quality reports:
```python
from excel_to_sql.auto_pilot import QualityScorer

scorer = QualityScorer()
report = scorer.generate_quality_report(df, "table_name")

# Returns:
# {
#     "score": 92,
#     "grade": "A",
#     "issues": [...],
#     "column_stats": {...}
# }
```

**RecommendationEngine** - Provides prioritized recommendations:
```python
from excel_to_sql.auto_pilot import RecommendationEngine

engine = RecommendationEngine()
recommendations = engine.generate_recommendations(
    df, "table_name", quality_report, patterns
)

# Returns prioritized recommendations (HIGH/MEDIUM/LOW)
```

**AutoFixer** - Automatically fixes data quality issues:
```python
from excel_to_sql.auto_pilot import AutoFixer

fixer = AutoFixer()
result = fixer.apply_auto_fixes(
    df, file_path, "Sheet1", recommendations, dry_run=False
)

# Automatically fixes:
# - Null values with smart defaults
# - French codes (ENTRÉE→inbound, etc.)
# - Split fields with COALESCE
```

**InteractiveWizard** - Guided configuration:
```python
from excel_to_sql.ui import InteractiveWizard

wizard = InteractiveWizard()
result = wizard.run_interactive_mode(
    excel_files, patterns_dict, quality_dict, output_path
)
```

### Auto-Fix Capabilities

Auto-Pilot can automatically fix common data quality issues:

**Null Value Fixing:**
- Fills nulls with smart defaults ("0", "CURRENT_TIMESTAMP", "Other")
- Detects optimal default values from existing data
- Preserves data integrity

**French Code Translation:**
- ENTRÉE → inbound
- SORTIE → outbound
- ACTIF → active
- INACTIF → inactive
- And 7 more common mappings

**Split Field Combination:**
- Combines redundant status columns
- Uses COALESCE for intelligent fallback
- Example: `etat_superieur`, `etat_inferieur` → `status`

### When to Use Auto-Pilot

✅ **Perfect for:**
- Quick prototyping and testing
- Ad-hoc data imports
- Exploring new datasets
- Learning the tool
- Small to medium datasets

❌ **Not ideal for:**
- Production deployments (use generated config as template)
- Complex custom transformations
- Highly specialized business logic
- Performance-critical operations

### Best Practices

1. **Start with Auto-Pilot** - Generate initial configuration automatically
2. **Review Generated Config** - Verify detected patterns and mappings
3. **Use Interactive Mode** - For complex datasets, review each file
4. **Customize as Needed** - Edit the generated mappings.json for your needs
5. **Test Before Production** - Always test with sample data first

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

## 🎉 Version 0.3.0 Highlights

**Auto-Pilot Mode - Zero-Configuration Import:**
1. ✅ **Pattern Detection** - Automatic detection of PKs, FKs, value mappings, split fields
2. ✅ **Quality Scoring** - Multi-dimensional data quality analysis with grades (A-D)
3. ✅ **Smart Recommendations** - Prioritized, actionable suggestions (HIGH/MEDIUM/LOW)
4. ✅ **Auto-Fix Capabilities** - One-click corrections for common data issues
5. ✅ **Interactive Wizard** - Step-by-step guided configuration workflow
6. ✅ **French Code Support** - Automatic translation (ENTRÉE→inbound, etc.)
7. ✅ **Split Field Detection** - Intelligent COALESCE for redundant columns
8. ✅ **CLI Integration** - `magic` command with --interactive flag

**Under the Hood:**
- **PatternDetector** (97% coverage) - Intelligent pattern recognition
- **QualityScorer** (99% coverage) - Comprehensive quality analysis
- **RecommendationEngine** (92% coverage) - Smart recommendations
- **AutoFixer** (88% coverage) - Automatic data fixing with backup system
- **InteractiveWizard** (54% coverage) - Rich terminal UI with guided flow

**Testing:**
- 143+ tests for Auto-Pilot components
- Integration tests with real Excel fixtures
- >85% coverage for core Auto-Pilot modules

**Previous Features (v0.2.0):**
- Value Mapping, Calculated Columns, Custom Validators
- Data Profiling & Quality Reports
- Multi-Sheet Import/Export
- Incremental Import with UPSERT
- Python SDK & Programmatic API

**Total: 200+ tests** with comprehensive coverage across all features.
