"""
Create test fixtures including sample Excel files.
"""

import pandas as pd
from pathlib import Path


def create_sample_excel():
    """Create a sample Excel file for testing."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    fixtures_dir.mkdir(exist_ok=True)

    # Create sample data with various types
    data = {
        "ID": [1, 2, 3, 4, 5],
        "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "Age": [25, 30, 35, 28, 32],
        "Salary": [50000.50, 60000.00, 70000.50, 55000.00, 65000.00],
        "Active": [True, True, False, True, False],
        "Join Date": pd.to_datetime(["2020-01-15", "2019-03-20", "2021-07-01", "2020-11-11", "2022-02-28"]),
    }

    df = pd.DataFrame(data)

    # Write to Excel
    output_path = fixtures_dir / "sample_data.xlsx"
    df.to_excel(output_path, index=False, sheet_name="Employees")

    print(f"Created sample Excel file: {output_path}")

    return output_path


if __name__ == "__main__":
    create_sample_excel()
