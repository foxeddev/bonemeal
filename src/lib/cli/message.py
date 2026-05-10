from sys import stdout, stderr
from typing import Optional, TextIO

from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.styles import BaseStyle

from lib.cli.base import BORDER_VERTICAL
from lib.cli.component import base_component


def info_message(
    title: AnyFormattedText = None,
    description: AnyFormattedText = None,
    icon: AnyFormattedText = "i",
    line: AnyFormattedText = BORDER_VERTICAL,
    connect: bool = True,
    file: TextIO = stdout,
    style: Optional[BaseStyle] = None,
) -> None:
    """
    Default icon: `i`

    Style class: `info_message`
    """

    style_classes = ["info_message"]

    return base_component(
        title=title,
        description=description,
        icon=icon,
        line=line,
        connect=connect,
        file=file,
        style=style,
        style_classes=style_classes,
    )


def success_message(
    title: AnyFormattedText = None,
    description: AnyFormattedText = None,
    icon: AnyFormattedText = "*",
    line: AnyFormattedText = BORDER_VERTICAL,
    connect: bool = True,
    file: TextIO = stdout,
    style: Optional[BaseStyle] = None,
) -> None:
    """
    Default icon: `*`

    Style class: `success_message`
    """

    style_classes = ["success_message"]

    return base_component(
        title=title,
        description=description,
        icon=icon,
        line=line,
        connect=connect,
        file=file,
        style=style,
        style_classes=style_classes,
    )


def warning_message(
    title: AnyFormattedText = None,
    description: AnyFormattedText = None,
    icon: AnyFormattedText = "*",
    line: AnyFormattedText = BORDER_VERTICAL,
    connect: bool = True,
    file: TextIO = stdout,
    style: Optional[BaseStyle] = None,
) -> None:
    """
    Default icon: `!`

    Style class: `warning_message`
    """

    style_classes = ["warning_message"]

    return base_component(
        title=title,
        description=description,
        icon=icon,
        line=line,
        connect=connect,
        file=file,
        style=style,
        style_classes=style_classes,
    )


def error_message(
    title: AnyFormattedText = None,
    description: AnyFormattedText = None,
    icon: AnyFormattedText = "*",
    line: AnyFormattedText = BORDER_VERTICAL,
    file: TextIO = stderr,
    connect: bool = True,
    style: Optional[BaseStyle] = None,
) -> None:
    """
    Default icon: `!`

    Default file: `stderr`

    Style class: `error_message`
    """

    style_classes = ["error_message"]

    return base_component(
        title=title,
        description=description,
        icon=icon,
        line=line,
        connect=connect,
        file=file,
        style=style,
        style_classes=style_classes,
    )
