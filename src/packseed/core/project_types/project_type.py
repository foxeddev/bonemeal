"""The base class and registry for project types."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import rich_click
    from prompt_toolkit.formatted_text import AnyFormattedText


@dataclass(frozen=True, slots=True)
class ProjectType:
    """The base class for project types."""

    id: str
    name: str
    create: rich_click.Command
    title: AnyFormattedText
    aliases: list[str] | None = None
    description: AnyFormattedText = None
