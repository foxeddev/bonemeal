"""Utilities."""

import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import rich_click


def add_command(group: rich_click.RichGroup, command: rich_click.RichCommand) -> None:
    """Add a command to a command group while inheriting all properties."""
    group.add_command(
        cmd=command,
        name=command.name,
        aliases=command.aliases,
        panel=command.panel,
    )


def get_git_username() -> str | None:
    """Try to find the user's Git username or return None."""
    try:
        return subprocess.check_output(
            # this is fine because no sensitive data is passed
            ["git", "config", "user.name"],  # noqa: S607
            text=True,
        ).strip()

    except subprocess.CalledProcessError:
        return None
