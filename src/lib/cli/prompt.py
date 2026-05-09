from dataclasses import dataclass
import sys
from typing import Optional, TextIO

from prompt_toolkit.formatted_text import AnyFormattedText, merge_formatted_text
from prompt_toolkit.key_binding import KeyBindings, KeyBindingsBase, merge_key_bindings
from prompt_toolkit.layout import FormattedTextControl, Window
from prompt_toolkit.styles import BaseStyle
from prompt_toolkit.widgets import TextArea

from lib.cli.base import BORDER_VERTICAL, fmt
from lib.cli.component import base_component


def text_prompt(
    title: AnyFormattedText = None,
    description: AnyFormattedText = None,
    required: bool = False,
    cursor: AnyFormattedText = ">",
    icon: AnyFormattedText = "?",
    line: AnyFormattedText = BORDER_VERTICAL,
    connect: bool = True,
    file: TextIO = sys.stdout,
    style: Optional[BaseStyle] = None,
    key_bindings: Optional[KeyBindingsBase] = None,
) -> str:
    """
    Print a prompt with a single line text input field.

    Default icon: `?`

    Style class: `text_prompt`

    ### Output

    ```
    |
    ? Title
    | Description
    | > Input
    ```

    ### Arguments

    #### `cursor`

    Text to be displayed as a prefix before the input field. Defaults to `>`.

    #### `required`

    Whether an empty input should not be allowed. Defaults to False.
    """

    style_classes = ["text_prompt"]

    cursor = fmt(cursor, ["cursor", *style_classes])
    line = fmt(line, ["line", *style_classes])

    def get_line_prefix(*_):
        return merge_formatted_text([line, fmt(" "), cursor, fmt(" ")])

    input_field = TextArea(
        multiline=False,
        get_line_prefix=get_line_prefix,
        style=fmt("", ["input", *style_classes])[0][0],
    )

    component_key_bindings = KeyBindings()

    @component_key_bindings.add("enter")
    def _(event):
        if input_field.text or not required:
            event.app.exit(result=input_field.text, style="class:confirmed")

    key_bindings = merge_key_bindings(
        [
            component_key_bindings,
            *([key_bindings] if key_bindings else []),
        ]
    )

    return base_component(
        content=input_field,
        title=title,
        description=description,
        icon=icon,
        line=line,
        connect=connect,
        interactive=True,
        file=file,
        style=style,
        key_bindings=key_bindings,
        style_classes=style_classes,
    )


@dataclass
class Option:
    title: AnyFormattedText
    description: AnyFormattedText = None


def option_prompt(
    options: list[Option],
    title: AnyFormattedText = None,
    description: AnyFormattedText = None,
    default_option: int = 0,
    cursor: AnyFormattedText = ">",
    icon: AnyFormattedText = "?",
    line: AnyFormattedText = BORDER_VERTICAL,
    connect: bool = True,
    file: TextIO = sys.stdout,
    style: Optional[BaseStyle] = None,
    key_bindings: Optional[KeyBindingsBase] = None,
) -> int:
    """
    Print a prompt with a list of options.

    Default icon: `?`

    Style class: `option_prompt`

    ### Output

    ```
    |
    ? Title
    | Description
    | > Option
    |   Option
    ```

    ### Arguments

    #### `options`

    List of options.

    #### `cursor`

    Text to be displayed as a prefix before the input field. Defaults to `>`.
    """

    style_classes = ["option_prompt"]

    hovered_option: int = default_option

    cursor = fmt(cursor, ["cursor", *style_classes])
    line = fmt(line, ["line", *style_classes])

    def get_option_text():
        return merge_formatted_text(
            [
                merge_formatted_text(
                    [
                        cursor if i == hovered_option else fmt(" "),
                        fmt(" "),
                        fmt(
                            option.title,
                            [
                                "option_title",
                                *style_classes,
                            ],
                        ),
                        *(
                            [
                                fmt("\n  "),
                                fmt(
                                    option.description,
                                    ["option_description", *style_classes],
                                ),
                            ]
                            if option.description
                            else []
                        ),
                        fmt("\n") if not i == len(options) - 1 else None,
                    ]
                )
                for i, option in enumerate(options)
            ],
        )

    def get_line_prefix(*_):
        return merge_formatted_text([line, fmt(" ")])

    option_field = Window(
        FormattedTextControl(get_option_text),
        always_hide_cursor=True,
        get_line_prefix=get_line_prefix,
    )

    component_key_bindings = KeyBindings()

    @component_key_bindings.add("up")
    def _(_):
        nonlocal hovered_option
        if hovered_option > 0:
            hovered_option -= 1

    @component_key_bindings.add("down")
    def _(_):
        nonlocal hovered_option
        if hovered_option < len(options) - 1:
            hovered_option += 1

    @component_key_bindings.add("enter")
    def _(event):
        event.app.exit(result=hovered_option)

    key_bindings = merge_key_bindings(
        [
            component_key_bindings,
            *([key_bindings] if key_bindings else []),
        ]
    )

    return base_component(
        content=option_field,
        title=title,
        description=description,
        icon=icon,
        line=line,
        connect=connect,
        interactive=True,
        file=file,
        style=style,
        key_bindings=key_bindings,
        style_classes=style_classes,
    )
