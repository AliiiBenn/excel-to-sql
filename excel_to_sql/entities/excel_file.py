"""
Excel file entity for reading and hashing Excel files.

Encapsulates file I/O and content-based hashing for incremental imports.
"""

from pathlib import Path
from typing import Optional

import pandas as pd
import hashlib


class ExcelFile:
    """
    Represents an Excel file with reading and hashing capabilities.

    Usage:
        file = ExcelFile("path/to/file.xlsx")
        df = file.read()                    # Read as DataFrame
        hash_value = file.content_hash      # Get SHA-256 of content
    """

    def __init__(self, path: Path | str) -> None:
        """
        Initialize Excel file entity.

        Args:
            path: Path to Excel file
        """
        self._path = Path(path)
        self._hash_cache: Optional[str] = None

    # ──────────────────────────────────────────────────────────────
    # PROPERTIES
    # ──────────────────────────────────────────────────────────────

    @property
    def path(self) -> Path:
        """File path."""
        return self._path

    @property
    def name(self) -> str:
        """Filename with extension."""
        return self._path.name

    @property
    def exists(self) -> bool:
        """Check if file exists."""
        return self._path.exists()

    @property
    def content_hash(self) -> str:
        """
        SHA-256 hash of DataFrame content (not file bytes).

        Lazy computation - cached after first call.
        Hash is based on:
        - Column names (sorted)
        - Row values (converted to string)
        - NOT file metadata (mtime, size)

        This means: Same data = Same hash, even if file recreated.
        """
        if self._hash_cache is None:
            df = self.read()
            self._hash_cache = self._compute_hash(df)
        return self._hash_cache

    # ──────────────────────────────────────────────────────────────
    # PUBLIC METHODS
    # ──────────────────────────────────────────────────────────────

    def read(self, sheet_name: str | None = None) -> pd.DataFrame:
        """
        Read Excel file as DataFrame.

        Args:
            sheet_name: Sheet to read (default: first sheet)

        Returns:
            Pandas DataFrame with raw data

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is invalid/corrupted
        """
        if not self.exists:
            raise FileNotFoundError(f"Excel file not found: {self._path}")

        if self._path.suffix.lower() not in {".xlsx", ".xls"}:
            raise ValueError(f"Not an Excel file: {self._path}")

        try:
            return pd.read_excel(self._path, sheet_name=sheet_name, engine="openpyxl")
        except Exception as e:
            raise ValueError(f"Failed to read Excel file: {e}") from e

    def validate(self) -> bool:
        """
        Quick validation that file is readable.

        Returns:
            True if file can be read

        Doesn't load full data - just checks:
        - File exists
        - Has .xlsx extension
        - Can read sheet names
        """
        if not self.exists:
            return False

        if self._path.suffix.lower() not in {".xlsx", ".xls"}:
            return False

        try:
            pd.ExcelFile(self._path, engine="openpyxl")
            return True
        except Exception:
            return False

    # ──────────────────────────────────────────────────────────────
    # PRIVATE METHODS
    # ──────────────────────────────────────────────────────────────

    def _compute_hash(self, df: pd.DataFrame) -> str:
        """
        Compute hash of DataFrame content.

        Args:
            df: DataFrame to hash

        Returns:
            Hexadecimal SHA-256 hash

        Hash computation strategy:
        - Sort columns for consistency
        - Convert to string representation
        - Hash the resulting string

        This ensures that same data produces same hash,
        regardless of original column order.
        """
        # Sort columns for consistency
        df_sorted = df[sorted(df.columns)]

        # Convert to string representation
        content_str = df_sorted.to_string(index=True)

        # Compute SHA-256
        return hashlib.sha256(content_str.encode()).hexdigest()
