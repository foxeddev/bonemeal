"""Utilities for the CLI library."""

import enum

from prompt_toolkit.formatted_text import (
    AnyFormattedText,
    FormattedText,
    to_formatted_text,
)
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.styles import BaseStyle, Style

BORDER_VERTICAL = "\u2502"


class LineMode(enum.Enum):
    """Whether an additional line should be added before the component.

    Used to add visual connection between multiple components.
    """

    OPEN_START = enum.auto()
    CLOSED_START = enum.auto()


class ComponentMode(enum.Enum):
    """Whether a component should automatically exit after printing or stay interactive.

    `interactive` should only be used if `content` is specified.
    """

    AUTO_EXIT = enum.auto()
    INTERACTIVE = enum.auto()


DEFAULT_STYLE: BaseStyle = Style(
    [
        ("description", "dim"),
        ("icon", "bold"),
        ("icon info_message", "ansiblue"),
        ("icon success_message", "ansigreen"),
        ("icon warning_message", "ansiyellow"),
        ("icon error_message", "ansired"),
        ("icon text_prompt", "ansiblue"),
        ("icon single_option_prompt", "ansiblue"),
        ("icon multi_option_prompt", "ansiblue"),
        ("option_description", "dim"),
    ],
)


DEFAULT_KEY_BINDINGS = KeyBindings()


@DEFAULT_KEY_BINDINGS.add("c-c")
def _(event: KeyPressEvent) -> None:
    event.app.exit(exception=KeyboardInterrupt)


def merge_style_strings(styles: list[str]) -> str:
    """Merge (Concatenate) several style strings together."""
    return " ".join(style for style in styles)


def fmt(
    text: AnyFormattedText,
    classes: str | list[str] | None = None,
) -> FormattedText:
    """Convert the given formatted text into a list of text fragments.

    ### Arguments

    #### `classes`

    Additional style classes to apply to all text fragments.
    """
    return (
        to_formatted_text(
            text,
            style=(merge_style_strings([f"class:{cls}" for cls in classes])),
        )
        if classes
        else to_formatted_text(text)
    )
