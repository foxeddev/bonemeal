from typing import Optional

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import (
    AnyFormattedText,
    FormattedText,
    split_lines,
    to_formatted_text,
)
from prompt_toolkit.styles import BaseStyle, merge_styles

from lib.cli.base import DEFAULT_STYLE, BORDER_VERTICAL


def base_message(
    message,
    details: AnyFormattedText = None,
    icon: AnyFormattedText = None,
    line: AnyFormattedText = BORDER_VERTICAL,
    extend: int = 1,
    style: Optional[BaseStyle] = None,
    style_classes: Optional[str | list[str]] = None,
):
    """
    ## Example

    ```
    * Message
    | Details
    |
    ```

    ## Params

    ### `message`

    The message to display.

    Style class: `message`

    ### `details`

    (optional) Additional details to display below the message.

    Style class: `details`

    ### `icon`

    Text to display as a prefix before the message. Should be a single character. Defaults to `*`.

    Style class: `icon`

    ### `line`

    Text to display to the left of the component. Should be a single character. Defaults to `|`.

    Style class: `line`

    ### `extend`

    How many additional lines should be added after the component. Can be used to add spacing between multiple component. Defaults to `1`.

    ### `style`

    (optional) Style to apply to the whole message.

    ### `style_classes`

    (optional) Additional style classes to add to all text fragments.
    """

    style = merge_styles([DEFAULT_STYLE, style]) if style else DEFAULT_STYLE

    if style_classes is None:
        style_classes = []
    elif type(style_classes) is str:
        style_classes = [style_classes]

    def fmt(text: AnyFormattedText, classes: Optional[str | list[str]] = None):
        return to_formatted_text(
            text, style=(" ".join(f"class:{cls}" for cls in classes)) if classes else ""
        )

    fmt_message = fmt(message, ["message", *style_classes])
    fmt_details = fmt(details, ["details", *style_classes])
    fmt_icon = fmt(icon, ["icon", *style_classes])
    fmt_line = fmt(line, ["line", *style_classes])

    result = FormattedText()

    for i, line_content in enumerate(split_lines(fmt_message)):
        line_content = FormattedText(line_content)
        result.extend(fmt_icon or fmt_line if i == 0 else fmt_line)
        result.extend(fmt(" "))
        result.extend(line_content)
        result.extend(fmt("\n"))

    if details:
        for line_content in split_lines(fmt_details):
            result.extend(fmt_line)
            result.extend(fmt(" "))
            result.extend(line_content)
            result.extend(fmt("\n"))

    for _ in range(extend):
        result.extend(fmt_line)
        result.extend(fmt("\n"))

    print_formatted_text(result, end="", style=style)


def info_message(
    message,
    details: AnyFormattedText = None,
    icon: AnyFormattedText = "i",
    line: AnyFormattedText = BORDER_VERTICAL,
    extend: int = 1,
    style: Optional[BaseStyle] = None,
):
    """
    Message with a blue `i` as an icon.

    Style class: `info`
    """
    base_message(
        message=message,
        details=details,
        icon=icon,
        line=line,
        extend=extend,
        style=style,
        style_classes="info",
    )


def success_message(
    message,
    details: AnyFormattedText = None,
    icon: AnyFormattedText = "*",
    line: AnyFormattedText = BORDER_VERTICAL,
    extend: int = 1,
    style: Optional[BaseStyle] = None,
):
    """
    Message with green `*` as an icon.

    Style class: `success`
    """
    base_message(
        message=message,
        details=details,
        icon=icon,
        line=line,
        extend=extend,
        style=style,
        style_classes="success",
    )


def warning_message(
    message,
    details: AnyFormattedText = None,
    icon: AnyFormattedText = "!",
    line: AnyFormattedText = BORDER_VERTICAL,
    extend: int = 1,
    style: Optional[BaseStyle] = None,
):
    """
    Message with a yellow `!` as an icon.

    Style class: `warning`
    """

    base_message(
        message=message,
        details=details,
        icon=icon,
        line=line,
        extend=extend,
        style=style,
        style_classes="warning",
    )


def error_message(
    message,
    details: AnyFormattedText = None,
    icon: AnyFormattedText = "!",
    line: AnyFormattedText = BORDER_VERTICAL,
    extend: int = 1,
    style: Optional[BaseStyle] = None,
):
    """
    Message with a red `!` as an icon.

    Style class: `error`
    """

    base_message(
        message=message,
        details=details,
        icon=icon,
        line=line,
        extend=extend,
        style=style,
        style_classes="error",
    )
