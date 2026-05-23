"""Command for listing all possible project types."""

import rich_click

from packseed.cli.components.message import info_message
from packseed.cli.components.utils import LineMode
from packseed.cli.errors import handle_errors
from packseed.core.project_types.main import PROJECT_TYPES


@rich_click.command("list")
@handle_errors
def list_project_types() -> None:
    """List all possible project types."""
    for project_type in PROJECT_TYPES.values():
        info_message(
            project_type.title,
            project_type.description,
            line=None,
            line_mode=LineMode.CLOSED_START,
        )
