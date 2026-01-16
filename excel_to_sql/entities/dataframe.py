"""
DataFrame wrapper entity for cleaning and transformation.

Encapsulates data cleaning, column mapping, and type conversion logic.
"""

from typing import Optional

import pandas as pd
import numpy as np


class DataFrame:
    """
    Wrapper around pandas.DataFrame with cleaning and transformation.

    Usage:
        df = DataFrame(raw_df)
        df.clean()
        df.apply_mapping(mapping)
        result = df.to_pandas()
    """

    def __init__(self, data: Optional[pd.DataFrame] = None) -> None:
        """
        Initialize DataFrame wrapper.

        Args:
            data: Existing DataFrame or None for empty DataFrame
        """
        if data is None:
            self._df = pd.DataFrame()
        else:
            self._df = data.copy()

    # ──────────────────────────────────────────────────────────────
    # PROPERTIES
    # ──────────────────────────────────────────────────────────────

    @property
    def columns(self) -> list[str]:
        """Column names."""
        return self._df.columns.tolist()

    @property
    def shape(self) -> tuple[int, int]:
        """(rows, columns) dimensions."""
        return self._df.shape

    @property
    def is_empty(self) -> bool:
        """True if no rows."""
        return len(self._df) == 0

    # ──────────────────────────────────────────────────────────────
    # PUBLIC METHODS
    # ──────────────────────────────────────────────────────────────

    def clean(self, strip_columns: bool = True) -> None:
        """
        Clean data in place.

        Transformations:
        1. Strip whitespace from string columns
        2. Normalize empty strings to NaN
        3. Drop completely empty rows
        4. Convert column names to lowercase

        Args:
            strip_columns: If True, strip column names too

        Example:
            Before: ["  Name  ", "Date", ""]
            After:  ["name", "date", NaN]
        """
        df = self._df

        # 1. Strip whitespace from string columns
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].astype(str).str.strip()

        # 2. Normalize empty strings to NaN
        df.replace(r"^\s*$", np.nan, regex=True, inplace=True)

        # 3. Drop completely empty rows
        df.dropna(how="all", inplace=True)

        # 4. Lowercase and strip column names
        if strip_columns:
            df.columns = df.columns.str.lower().str.strip()

    def apply_mapping(self, mapping: dict) -> None:
        """
        Apply column mapping and type conversion.

        Args:
            mapping: Dictionary from mappings.json

        Mapping structure:
            {
                "target_table": "products",
                "primary_key": ["id"],
                "column_mappings": {
                    "ID": {"target": "id", "type": "integer"},
                    "Name": {"target": "name", "type": "string"},
                    "Price": {"target": "price", "type": "float"}
                }
            }

        What it does:
        1. Rename columns: ID -> id, Name -> name
        2. Drop unmapped columns
        3. Convert types according to mapping

        Example:
            Before: {"ID": [1, 2], "Name": ["A", "B"], "Ignore": ["X", "Y"]}
            After:  {"id": [1, 2], "name": ["A", "B"]}
        """
        column_mappings = mapping["column_mappings"]

        # Build rename dict: source -> target
        rename_dict = {}
        type_conversions = {}

        for source_col, config in column_mappings.items():
            target_col = config["target"]
            col_type = config.get("type", "string")

            rename_dict[source_col] = target_col
            type_conversions[target_col] = col_type

        # Rename columns
        self._df = self._df.rename(columns=rename_dict)

        # Keep only mapped columns
        mapped_columns = list(rename_dict.values())
        self._df = self._df[mapped_columns]

        # Convert types
        for col, col_type in type_conversions.items():
            if col_type == "integer":
                self._df[col] = pd.to_numeric(self._df[col], errors="coerce").astype(
                    "Int64"
                )
            elif col_type == "float":
                self._df[col] = pd.to_numeric(self._df[col], errors="coerce")
            elif col_type == "boolean":
                self._df[col] = self._df[col].map(
                    {
                        "TRUE": True,
                        "FALSE": False,
                        "1": True,
                        "0": False,
                        True: True,
                        False: False,
                        1: True,
                        0: False,
                    }
                )
            elif col_type == "date":
                self._df[col] = pd.to_datetime(self._df[col], errors="coerce")
            # string is default (do nothing)

    def filter_nulls(self, columns: list[str]) -> None:
        """
        Remove rows where any of these columns are null.

        Args:
            columns: Columns to check for null values

        Example:
            df.filter_nulls(["id", "name"])
            # Removes rows where id OR name is null
        """
        self._df.dropna(subset=columns, inplace=True)

    def to_pandas(self) -> pd.DataFrame:
        """Get underlying pandas DataFrame."""
        return self._df.copy()

    def to_dict(self, orient: str = "records") -> list[dict]:
        """Convert to list of dictionaries."""
        return self._df.to_dict(orient=orient)
