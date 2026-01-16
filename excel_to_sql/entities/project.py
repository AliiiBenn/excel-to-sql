"""
Project entity for excel-to-sql.

Represents a project with its directories, configuration, and database.
"""

from pathlib import Path
from typing import Optional, Dict
import json


class Project:
    """
    Represents an excel-to-sql project.

    A project encapsulates:
    - Directory structure (imports/, exports/, data/)
    - Configuration (mappings.json)
    - Database connection
    - Settings and paths

    Usage:
        project = Project()
        project.initialize()

        # Or load existing
        project = Project.from_current_directory()
    """

    def __init__(self, root: Optional[Path] = None):
        """
        Initialize a Project.

        Args:
            root: Project root directory (auto-detected if None)
        """
        self._root = root or self._find_project_root()
        self._database = None
        self._mappings: Optional[dict] = None

    # ──────────────────────────────────────────────────────────────
    # PROPERTIES
    # ──────────────────────────────────────────────────────────────

    @property
    def root(self) -> Path:
        """Project root directory."""
        return self._root

    @property
    def imports_dir(self) -> Path:
        """Directory for Excel files to import."""
        return self._root / "imports"

    @property
    def exports_dir(self) -> Path:
        """Directory for generated Excel exports."""
        return self._root / "exports"

    @property
    def data_dir(self) -> Path:
        """Directory for database files."""
        return self._root / "data"

    @property
    def logs_dir(self) -> Path:
        """Directory for log files."""
        return self._root / "logs"

    @property
    def config_dir(self) -> Path:
        """Directory for configuration files."""
        return self._root / "config"

    @property
    def mappings_file(self) -> Path:
        """Path to mappings.json configuration."""
        return self.config_dir / "mappings.json"

    @property
    def database(self):
        """
        Get the Database entity for this project.
        Lazily created on first access.
        """
        if self._database is None:
            from excel_to_sql.entities.database import Database

            db_path = self.data_dir / "warehouse.db"
            self._database = Database(db_path)
        return self._database

    @property
    def mappings(self) -> dict:
        """
        Load and return mappings configuration.
        Returns empty dict if file doesn't exist.
        """
        if self._mappings is None:
            self._mappings = self._load_mappings()
        return self._mappings

    # ──────────────────────────────────────────────────────────────
    # CLASS METHODS
    # ──────────────────────────────────────────────────────────────

    @classmethod
    def from_current_directory(cls) -> "Project":
        """
        Create a Project from current working directory.
        Auto-detects project root by looking for markers (.git, pyproject.toml)

        Returns:
            Project instance
        """
        return cls(root=None)  # None triggers auto-detection

    # ──────────────────────────────────────────────────────────────
    # PUBLIC METHODS
    # ──────────────────────────────────────────────────────────────

    def initialize(self, force: bool = False) -> None:
        """
        Initialize project structure.
        Creates directories, database, and default configuration.

        Args:
            force: Re-initialize even if already initialized
        """
        # Create directories
        for directory in [
            self.imports_dir,
            self.exports_dir,
            self.data_dir,
            self.logs_dir,
            self.config_dir,
        ]:
            directory.mkdir(parents=True, exist_ok=True)

        # Initialize database
        self.database.initialize()

        # Create default mappings if doesn't exist
        if not self.mappings_file.exists() or force:
            self._create_default_mappings()

    def add_mapping(
        self,
        type_name: str,
        table_name: str,
        primary_key: list[str],
        column_mappings: dict,
    ) -> None:
        """
        Add a new type mapping to configuration.

        Args:
            type_name: Name of the type (e.g., "orders", "picking_lines")
            table_name: Target SQL table name
            primary_key: List of primary key columns
            column_mappings: Dict of column mappings
        """
        mappings = self.mappings
        mappings[type_name] = {
            "target_table": table_name,
            "primary_key": primary_key,
            "column_mappings": column_mappings,
        }
        self._save_mappings(mappings)
        self._mappings = None  # Clear cache

    def get_mapping(self, type_name: str) -> Optional[dict]:
        """Get a specific type mapping."""
        return self.mappings.get(type_name)

    def list_types(self) -> list[str]:
        """List all configured types."""
        return list(self.mappings.keys())

    # ──────────────────────────────────────────────────────────────
    # PRIVATE METHODS
    # ──────────────────────────────────────────────────────────────

    def _find_project_root(self) -> Path:
        """Auto-detect project root by looking for markers."""
        # Start from current file location and go up
        current = Path(__file__).resolve().parent.parent.parent

        # Check if we have markers in current directory
        for _ in range(5):
            if (
                (current / ".git").exists()
                or (current / "pyproject.toml").exists()
                or (current / ".python-version").exists()
            ):
                return current
            current = current.parent

        # Fallback to current working directory
        return Path.cwd()

    def _load_mappings(self) -> dict:
        """Load mappings from JSON file."""
        if not self.mappings_file.exists():
            return {}

        with open(self.mappings_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_mappings(self, mappings: dict) -> None:
        """Save mappings to JSON file."""
        with open(self.mappings_file, "w", encoding="utf-8") as f:
            json.dump(mappings, f, indent=2, ensure_ascii=False)

    def _create_default_mappings(self) -> None:
        """Create default mappings configuration."""
        default_mappings = {
            "_example": {
                "description": "Example mapping - copy this structure for your types",
                "target_table": "example_table",
                "primary_key": ["id"],
                "column_mappings": {
                    "ID": {"target": "id", "type": "integer", "required": True},
                    "Name": {"target": "name", "type": "string", "required": False},
                },
            }
        }
        self._save_mappings(default_mappings)
