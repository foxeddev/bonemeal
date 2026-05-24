"""The base class and registry for project types."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    import rich_click
    from prompt_toolkit.formatted_text import AnyFormattedText


@dataclass(frozen=True, slots=True)
class ProjectType:
    """The base class for project types."""

    title: AnyFormattedText
    create: Callable[..., None]
    create_cmd: rich_click.RichCommand
    description: AnyFormattedText = None
