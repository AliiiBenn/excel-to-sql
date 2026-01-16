"""
Pydantic models for mapping configuration.

Provides validation and type safety for column mappings.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Literal


class ColumnMapping(BaseModel):
    """Configuration for a single column mapping."""

    target: str = Field(..., description="Target column name in database")
    type: Literal["string", "integer", "float", "boolean", "date"] = Field(
        default="string",
        description="SQL type for the column",
    )
    required: bool = Field(
        default=False, description="Whether null values should be rejected"
    )
    default: Optional[Any] = Field(
        default=None, description="Default value if column is missing"
    )


class TypeMapping(BaseModel):
    """Configuration for a file type."""

    target_table: str = Field(..., description="Destination table name")
    primary_key: List[str] = Field(
        ..., description="Primary key columns (for UPSERT)"
    )
    column_mappings: Dict[str, ColumnMapping] = Field(
        ..., description="Map of Excel column names to their configuration"
    )


class Mappings(BaseModel):
    """Root container for all mappings."""

    mappings: Dict[str, TypeMapping]

    def get_type(self, type_name: str) -> TypeMapping | None:
        """
        Get a specific type mapping.

        Args:
            type_name: Name of the type mapping

        Returns:
            TypeMapping or None if not found
        """
        return self.mappings.get(type_name)

    def list_types(self) -> list[str]:
        """List all configured type names."""
        return list(self.mappings.keys())
