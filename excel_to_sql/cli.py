"""
CLI interface for excel-to-sql using Typer.
"""

from typer import Typer, Option
from rich.console import Console

from excel_to_sql.entities.project import Project

app = Typer(
    name="excel-to-sql",
    help="Excel to SQL CLI - Import Excel files to SQL and export back",
    no_args_is_help=True,
    add_completion=False,
)

console = Console()


# ──────────────────────────────────────────────────────────────
# Command: INIT
# ──────────────────────────────────────────────────────────────


@app.command()
def init(
    db_path: str = Option("data/warehouse.db", "--db-path", help="Path to SQLite database"),
) -> None:
    """Initialize project structure and database."""
    console.print("[bold cyan]Initializing excel-to-sql project...[/bold cyan]")

    project = Project()
    project.initialize()

    console.print("[green]✓[/green] Project initialized successfully")
    console.print(f"  Location: {project.root}")
    console.print(f"  Database: {project.database.path}")
    console.print(f"  Imports:  {project.imports_dir}")
    console.print(f"  Exports:  {project.exports_dir}")


# ──────────────────────────────────────────────────────────────
# Command: IMPORT
# ──────────────────────────────────────────────────────────────


@app.command()
def import_cmd(
    excel_path: str = Option(..., "--file", "-f", help="Path to Excel file"),
    type: str = Option(..., "--type", "-t", help="Type configuration from mappings"),
    force: bool = Option(False, "--force", help="Re-import even if content unchanged"),
) -> None:
    """Import an Excel file into the database."""
    console.print(f"[bold cyan]Importing {excel_path}...[/bold cyan]")

    # TODO: Phase 3 - Implement full import logic
    console.print("[yellow]Command not implemented yet[/yellow]")
    console.print("  This will be implemented in Phase 3")


# ──────────────────────────────────────────────────────────────
# Command: EXPORT
# ──────────────────────────────────────────────────────────────


@app.command()
def export_cmd(
    output: str = Option(..., "--output", "-o", help="Output Excel file path"),
    table: str = Option(None, "--table", help="Export entire table"),
    query: str = Option(None, "--query", help="Custom SQL query"),
) -> None:
    """Export data from database to Excel."""
    if not table and not query:
        console.print("[red]Error:[/red] Must specify --table or --query")
        raise typer.Exit(1)

    console.print(f"[bold cyan]Exporting to {output}...[/bold cyan]")

    # TODO: Phase 4 - Implement export logic
    console.print("[yellow]Command not implemented yet[/yellow]")
    console.print("  This will be implemented in Phase 4")


# ──────────────────────────────────────────────────────────────
# Command: STATUS
# ──────────────────────────────────────────────────────────────


@app.command()
def status() -> None:
    """Show import history."""
    console.print("[bold cyan]Import Status:[/bold cyan]")

    # TODO: Phase 4 - Implement status display
    console.print("[dim]No imports yet[/dim]")


# ──────────────────────────────────────────────────────────────
# Command: CONFIG
# ──────────────────────────────────────────────────────────────


@app.command()
def config_cmd(
    add_type: str = Option(None, "--add-type", help="Add new type configuration"),
    table: str = Option(None, "--table", help="Target table name"),
) -> None:
    """Manage configuration mappings."""
    if add_type and table:
        console.print(f"[bold cyan]Adding type: {add_type} → {table}[/bold cyan]")
        # TODO: Phase 5 - Implement config logic
        console.print("[yellow]Command not implemented yet[/yellow]")
    else:
        console.print("[yellow]Usage: --add-type <name> --table <table>[/yellow]")


# ──────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app()
