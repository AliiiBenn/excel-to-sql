# Analysis of Issue #42 - Headers Not Detected Correctly

## Current Branch
`analyze-issue-42`

---

## Problem Summary

When using the Auto-Pilot command (`excel-to-sql magic`), French column headers are not detected correctly, resulting in column mappings named `Unnamed: 0`, `Unnamed: 1`, etc.

---

## Root Cause Identified

### Problematic Code Location

**File:** `excel_to_sql/cli.py`
**Lines:** 535, 622, 807

#### 1. DataFrame Reading (line 535)
```python
df = pd.read_excel(excel_file, sheet_name=sheet_name)
```

#### 2. Column Mappings Generation (lines 807-815)
```python
df = pd.read_excel(result["file"], sheet_name=result["sheet"])
for col in df.columns:
    col_type = _infer_sql_type(df[col])
    column_mappings[str(col)] = {
        "target": str(col),
        "type": col_type,
        "required": False,
        "default": None,
    }
```

#### 3. ExcelFile Class (excel_to_sql/entities/excel_file.py, line 91)
```python
return pd.read_excel(self._path, sheet_name=actual_sheet, engine="openpyxl")
```

---

## Technical Explanation

### The Problem

When an Excel file doesn't explicitly specify which rows are headers, pandas uses `header=0` by default (first row as header). However, in some cases:

1. **Headers with special characters**: Names like `"No. du produit"`, `"État"`, `"Catégorie de produit #1"` may cause encoding issues
2. **Empty or missing headers**: If the first row contains empty values or duplicates
3. **Poor automatic detection**: pandas may not correctly recognize header rows

### Why "Unnamed: X" Appears

When pandas reads an Excel file with `header=0` (default) and the first row contains numeric data instead of strings, OR if the first row values are empty/invalid:

- pandas generates default column names: `Unnamed: 0`, `Unnamed: 1`, etc.
- The real French headers get treated as data in the first DataFrame row

### Concrete Example

If the Excel file looks like:

| (row 0) | No. du produit | Nom du produit | Description |
|---------|----------------|----------------|-------------|
| (row 1) | 2725 | SHOEI MENTONNIERE | SHOEI... |
| (row 2) | 7353 | SHOEI CACHENEZ | SHOEI... |

If pandas detects that row 0 doesn't look like headers (because `"No. du produit"` contains special characters, or if encoding causes issues), it can:

1. Ignore row 0 as header
2. Generate `Unnamed: 0`, `Unnamed: 1`, `Unnamed: 2` as column names
3. Treat the real headers as data

---

## Specific Code to Fix

### File: `excel_to_sql/cli.py`

**Location 1 - Line 535** (`magic` function)
```python
df = pd.read_excel(excel_file, sheet_name=sheet_name)
```
→ No explicit `header` parameter

**Location 2 - Line 622** (interactive mode)
```python
df = pd.read_excel(file_path)
```
→ No explicit `header` parameter

**Location 3 - Line 807** (config generation)
```python
df = pd.read_excel(result["file"], sheet_name=result["sheet"])
```
→ No explicit `header` parameter

### File: `excel_to_sql/entities/excel_file.py`

**Location 4 - Line 91** (`ExcelFile` class)
```python
return pd.read_excel(self._path, sheet_name=actual_sheet, engine="openpyxl")
```
→ No explicit `header` parameter

---

## Dependency Analysis

### Impacted Modules

1. **`excel_to_sql/cli.py`** - `magic` command (Auto-Pilot)
2. **`excel_to_sql/entities/excel_file.py`** - `ExcelFile` class
3. **`excel_to_sql/auto_pilot/detector.py`** - Analyzes patterns (depends on correctly named columns)

### Execution Flow

```
cli.py:magic()
  → pd.read_excel(file, sheet_name) [without explicit header]
  → PatternDetector.detect_patterns(df, table_name)
  → Generates column_mappings using df.columns (which may contain "Unnamed: X")
```

---

## Why French Headers Fail

### Technical Hypotheses

1. **Character encoding**: Accents and special characters (`"État"`, `"No. du produit"`) may cause issues with `openpyxl` or pandas

2. **Insufficient automatic detection**: pandas uses a simple heuristic to detect headers. If first row values look like data (e.g., `"No. du produit"` can be interpreted as text data rather than a header)

3. **Excel file format**: The source file may have headers that don't start at row 0, or have empty rows before headers

---

## Suggested Solution (Not Implemented)

Issue #42 proposes a solution:

1. **Implement explicit header detection** that scans the first few rows
2. **Map French names to English** (e.g., `"No. du produit"` → `no_produit`)
3. **Generate configuration with explicit `header` parameter**

### Pseudocode (from the issue)

```python
def detect_header_row(file_path: Path) -> int:
    """Detect which row contains headers."""
    df = pd.read_excel(file_path, nrows=5, header=None)

    header_keywords = [
        "no_produit", "no. du produit", "produit",
        "nom_produit", "nom du produit", "description",
        "classe", "catégorie", "état", "configuration"
    ]

    for row_idx in range(min(5, len(df))):
        row_values = df.iloc[row_idx].astype(str).str.lower().str.strip()
        row_text = ' '.join(row_values)

        matches = sum(1 for keyword in header_keywords if keyword.lower() in row_text)

        if matches >= 3:
            return row_idx

    return None  # Default to header=0
```

---

## Tests to Confirm

### Reproduction Test

1. Create an Excel file with French headers (as described in the issue)
2. Run `excel-to-sql magic`
3. Verify if columns are named `Unnamed: X` instead of real names

### Test Code

```python
import pandas as pd
from pathlib import Path

# Test with the example file from the issue
df = pd.read_excel("produits.xlsx", sheet_name=0)

print("Detected columns:")
for i, col in enumerate(df.columns):
    print(f"  {i}: {col}")

# Expected:
#   0: No. du produit
#   1: Nom du produit
#   2: Description
#   ...

# Actual (bug):
#   0: Unnamed: 0
#   1: Unnamed: 1
#   2: Unnamed: 2
#   ...
```

---

## Analysis Status

✅ Root cause identified
✅ Problematic code located
✅ Technical explanation provided
✅ Reproduction tests defined

⚠️ **No fix has been applied** (as requested)

---

## Files to Modify to Fix the Bug

1. `excel_to_sql/cli.py` - Add `header` parameter to `pd.read_excel()` calls
2. `excel_to_sql/entities/excel_file.py` - Same
3. `excel_to_sql/auto_pilot/` - Add `detect_header_row()` function

---

## Additional Notes

- The problem specifically affects Excel files with French headers or special characters
- Impact is limited to the Auto-Pilot command (`magic`)
- Other commands (`import`, `export`) may also be affected if they depend on `ExcelFile.read()`
