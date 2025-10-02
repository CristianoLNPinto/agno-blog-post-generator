"""SQLite database configuration."""

from agno.db.sqlite import SqliteDb

from ...config import settings


def get_workflow_db() -> SqliteDb:
    """Get configured SQLite database for workflow."""
    return SqliteDb(
        session_table=settings.session_table,
        db_file=settings.db_file,
    )
