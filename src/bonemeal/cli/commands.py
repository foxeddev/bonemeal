"""Utilities for handling CLI commands."""

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
