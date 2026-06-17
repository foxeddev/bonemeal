"""Command for listing all available project types."""

import rich_click

from bonemeal.cli.components.message import info_message
from bonemeal.cli.components.utils import LineMode
from bonemeal.cli.utils.errors import handle_errors
from bonemeal.core.project_types.main import PROJECT_TYPES


@rich_click.command("list")
@handle_errors
def list_project_types() -> None:
    """List all available project types."""
    for project_type in PROJECT_TYPES.values():
        info_message(
            title=project_type.title,
            description=project_type.description,
            line=None,
            line_mode=LineMode.CLOSED_START,
        )
