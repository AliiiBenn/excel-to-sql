"""
CLI interface for excel-to-sql using Typer.
"""

from pathlib import Path
from typer import Typer, Option, Exit
from rich.console import Console
from rich.table import Table

from excel_to_sql.entities.project import Project
from excel_to_sql.entities.excel_file import ExcelFile
from excel_to_sql.entities.dataframe import DataFrame

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

    console.print("[green]OK[/green] Project initialized successfully")
    console.print(f"  Location: {project.root}")
    console.print(f"  Database: {project.database.path}")
    console.print(f"  Imports:  {project.imports_dir}")
    console.print(f"  Exports:  {project.exports_dir}")


# ──────────────────────────────────────────────────────────────
# Command: IMPORT
# ──────────────────────────────────────────────────────────────


@app.command("import")
def import_cmd(
    excel_path: str = Option(..., "--file", "-f", help="Path to Excel file"),
    type: str = Option(..., "--type", "-t", help="Type configuration from mappings"),
    force: bool = Option(False, "--force", help="Re-import even if content unchanged"),
) -> None:
    """Import an Excel file into the database."""
    import sys
    import traceback

    path = Path(excel_path)

    try:
        # 1. Validate file exists
        if not path.exists():
            console.print(f"[red]Error:[/red] File not found: {excel_path}")
            raise Exit(1)

        # 2. Validate file extension
        if path.suffix.lower() not in {".xlsx", ".xls"}:
            console.print(f"[red]Error:[/red] Not an Excel file: {excel_path}")
            raise Exit(1)

        # 3. Load project
        try:
            project = Project.from_current_directory()
        except Exception:
            console.print("[red]Error:[/red] Not an excel-to-sql project")
            console.print("  Run 'excel-to-sql init' first")
            raise Exit(1)

        # 4. Validate type exists
        if type not in project.mappings:
            console.print(f"[red]Error:[/red] Unknown type: '{type}'")
            available_types = ", ".join(project.list_types())
            console.print(f"  Available types: {available_types}")
            raise Exit(1)

        mapping = project.mappings[type]

        # 5. Load Excel file
        console.print(f"[bold cyan]Reading {excel_path}...[/bold cyan]")

        excel_file = ExcelFile(path)

        # Validate file is readable
        if not excel_file.validate():
            console.print("[red]Error:[/red] Invalid or corrupted Excel file")
            raise Exit(1)

        # Get content hash
        content_hash = excel_file.content_hash
        console.print(f"  Content hash: {content_hash[:16]}...")

        # 6. Check if already imported
        if not force and project.database.is_imported(content_hash):
            console.print("[yellow]Already imported[/yellow]")
            console.print("  Use --force to re-import")

            # Show previous import details
            history = project.database.query(
                "SELECT * FROM _import_history WHERE content_hash = :hash",
                {"hash": content_hash}
            )
            if len(history) > 0:
                record = history.iloc[0]
                console.print(f"  Imported: {record['imported_at']}")
                console.print(f"  Rows: {record['rows_imported']}")
            raise Exit(0)

        # 7. Read data
        console.print("[dim]Loading data...[/dim]")
        raw_df = excel_file.read()
        initial_rows = len(raw_df)
        console.print(f"  Rows loaded: {initial_rows}")

        # 8. Clean data
        console.print("[dim]Cleaning data...[/dim]")
        df_wrapper = DataFrame(raw_df)
        df_wrapper.clean()
        cleaned_rows = len(df_wrapper.to_pandas())
        rows_removed = initial_rows - cleaned_rows
        console.print(f"  Rows removed (empty): {rows_removed}")

        # 9. Apply mapping
        console.print("[dim]Applying mappings...[/dim]")
        df_wrapper.apply_mapping(mapping)
        final_df = df_wrapper.to_pandas()
        final_rows = len(final_df)
        console.print(f"  Columns: {len(final_df.columns)}")
        console.print(f"  Rows: {final_rows}")

        # 10. Import to database
        console.print("[dim]Importing to database...[/dim]")
        table = project.database.get_table(mapping["target_table"])
        stats = table.upsert(final_df, primary_key=mapping["primary_key"])
        console.print(f"  Inserted: {stats['inserted']}")
        console.print(f"  Updated: {stats['updated']}")

        # 11. Record import in history
        # If using --force and content_hash exists, delete old record first
        if force and project.database.is_imported(content_hash):
            project.database.execute(
                "DELETE FROM _import_history WHERE content_hash = :hash",
                {"hash": content_hash}
            )

        project.database.record_import(
            file_name=excel_file.name,
            file_path=str(path.absolute()),
            content_hash=content_hash,
            file_type=type,
            rows_imported=stats["inserted"] + stats["updated"],
            rows_skipped=0,
            status="success",
        )

        # 12. Display summary
        console.print()
        console.print("[green]OK[/green] Import completed successfully")

        summary_table = Table(show_header=True, title="Import Summary")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")

        summary_table.add_row("File", excel_file.name)
        summary_table.add_row("Type", type)
        summary_table.add_row("Table", mapping["target_table"])
        summary_table.add_row("Rows inserted", str(stats["inserted"]))
        summary_table.add_row("Rows updated", str(stats["updated"]))
        summary_table.add_row("Total rows", str(final_rows))
        summary_table.add_row("Content hash", content_hash[:16] + "...")

        console.print(summary_table)

    except FileNotFoundError:
        console.print(f"[red]Error:[/red] File not found: {excel_path}")
        raise Exit(1)

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise Exit(1)

    except Exit:
        # Re-raise Exit exceptions (they're intentional)
        raise

    except Exception as e:
        console.print(f"[red]Error:[/red] Import failed")
        console.print(f"  {e}")
        if "--debug" in sys.argv:
            console.print(traceback.format_exc())
        raise Exit(1)


# ──────────────────────────────────────────────────────────────
# Command: EXPORT
# ──────────────────────────────────────────────────────────────


@app.command("export")
def export_cmd(
    output: str = Option(..., "--output", "-o", help="Output Excel file path"),
    table: str = Option(None, "--table", help="Export entire table"),
    query: str = Option(None, "--query", help="Custom SQL query"),
) -> None:
    """Export data from database to Excel."""
    if not table and not query:
        console.print("[red]Error:[/red] Must specify --table or --query")
        raise Exit(1)

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
