"""Functions for printing some pre-styled messages."""

import sys
from typing import TYPE_CHECKING, TextIO

from packseed.cli.components.component import base_component
from packseed.cli.components.utils import BORDER_VERTICAL, ComponentMode, LineMode

if TYPE_CHECKING:
    from prompt_toolkit.formatted_text import AnyFormattedText
    from prompt_toolkit.styles import BaseStyle


def info_message(
    title: AnyFormattedText = None,
    description: AnyFormattedText = None,
    icon: AnyFormattedText = "i",
    line: AnyFormattedText = BORDER_VERTICAL,
    line_mode: LineMode = LineMode.OPEN_START,
    file: TextIO = sys.stdout,
    style: BaseStyle | None = None,
) -> None:
    """Print a formatted info message.

    Default icon: `i`

    Style class: `info_message`
    """
    style_classes = ["info_message"]

    base_component(
        title=title,
        description=description,
        icon=icon,
        line=line,
        line_mode=line_mode,
        component_mode=ComponentMode.AUTO_EXIT,
        file=file,
        style=style,
        style_classes=style_classes,
    )


def success_message(
    title: AnyFormattedText = None,
    description: AnyFormattedText = None,
    icon: AnyFormattedText = "*",
    line: AnyFormattedText = BORDER_VERTICAL,
    line_mode: LineMode = LineMode.OPEN_START,
    file: TextIO = sys.stdout,
    style: BaseStyle | None = None,
) -> None:
    """Print a formatted success message.

    Default icon: `*`

    Style class: `success_message`
    """
    style_classes = ["success_message"]

    base_component(
        title=title,
        description=description,
        icon=icon,
        line=line,
        line_mode=line_mode,
        component_mode=ComponentMode.AUTO_EXIT,
        file=file,
        style=style,
        style_classes=style_classes,
    )


def warning_message(
    title: AnyFormattedText = None,
    description: AnyFormattedText = None,
    icon: AnyFormattedText = "!",
    line: AnyFormattedText = BORDER_VERTICAL,
    line_mode: LineMode = LineMode.OPEN_START,
    file: TextIO = sys.stdout,
    style: BaseStyle | None = None,
) -> None:
    """Print a formatted warning message.

    Default icon: `!`

    Style class: `warning_message`
    """
    style_classes = ["warning_message"]

    base_component(
        title=title,
        description=description,
        icon=icon,
        line=line,
        line_mode=line_mode,
        component_mode=ComponentMode.AUTO_EXIT,
        file=file,
        style=style,
        style_classes=style_classes,
    )


def error_message(
    title: AnyFormattedText = None,
    description: AnyFormattedText = None,
    icon: AnyFormattedText = "*",
    line: AnyFormattedText = BORDER_VERTICAL,
    line_mode: LineMode = LineMode.OPEN_START,
    file: TextIO = sys.stderr,
    style: BaseStyle | None = None,
) -> None:
    """Print a formatted error message.

    Default icon: `!`

    Default file: `sys.stderr`

    Style class: `error_message`
    """
    style_classes = ["error_message"]

    base_component(
        title=title,
        description=description,
        icon=icon,
        line=line,
        line_mode=line_mode,
        component_mode=ComponentMode.AUTO_EXIT,
        file=file,
        style=style,
        style_classes=style_classes,
    )
