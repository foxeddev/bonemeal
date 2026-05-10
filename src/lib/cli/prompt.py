from dataclasses import dataclass
from sys import stdout
from typing import Any, Optional, TextIO

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
    file: TextIO = stdout,
    style: Optional[BaseStyle] = None,
    key_bindings: Optional[KeyBindingsBase] = None,
) -> str:
    """
    Print a prompt with a single line text input field.

    Default icon: `?`

    Style class: `text_prompt`

    Input field style class: `input`

    Confirmed style class: `confirmed`

    ### Output

    ```
    |
    ? Title
    | Description
    | > Input
    ```

    ### Arguments

    #### `cursor`

    Text to be displayed as a prefix before the input field.

    Default: `>`

    #### `required`

    Whether an empty input should not be allowed.

    Default: `False`
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
    value: Any
    title: AnyFormattedText
    description: AnyFormattedText = None


def single_option_prompt(
    options: list[Option],
    title: AnyFormattedText = None,
    description: AnyFormattedText = None,
    default_option: int = 0,
    cursor: AnyFormattedText = ">",
    icon: AnyFormattedText = "?",
    line: AnyFormattedText = BORDER_VERTICAL,
    connect: bool = True,
    file: TextIO = stdout,
    style: Optional[BaseStyle] = None,
    key_bindings: Optional[KeyBindingsBase] = None,
) -> int:
    """
    Print a prompt with a list of options where only one option can be selected at a time.

    Default icon: `?`

    Style class: `single_option_prompt`

    Confirmed style class: `confirmed`

    ### Output

    ```
    |
    ? Title
    | Description
    | > Option title
    |   Option description
    |   Option title
    ```

    ### Arguments

    #### `options`

    List of options.

    Style class: `option`

    Title style class: `option_title`

    Description style class: `option_description`

    Hovered style class: `hovered`

    #### `default_option`

    Index of the option selected when the component is created.

    Default: `0`

    #### `cursor`

    Text to be displayed as a prefix before the hovered option.

    Default: `>`
    """

    style_classes = ["single_option_prompt"]

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
                                "option",
                                "option_title",
                                *(["hovered"] if i == hovered_option else []),
                                *style_classes,
                            ],
                        ),
                        *(
                            [
                                fmt("\n  "),
                                fmt(
                                    option.description,
                                    [
                                        "option",
                                        "option_description",
                                        *(["hovered"] if i == hovered_option else []),
                                        *style_classes,
                                    ],
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
        event.app.exit(result=options[hovered_option].value, style="class:confirmed")

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


def multi_option_prompt(
    options: list[Option],
    title: AnyFormattedText = None,
    description: AnyFormattedText = None,
    cursor: AnyFormattedText = ">",
    selection_indicator: AnyFormattedText = "*",
    icon: AnyFormattedText = "?",
    line: AnyFormattedText = BORDER_VERTICAL,
    connect: bool = True,
    file: TextIO = stdout,
    style: Optional[BaseStyle] = None,
    key_bindings: Optional[KeyBindingsBase] = None,
) -> int:
    """
    Print a prompt with a list of options where multiple options can be selected at a time.

    Default icon: `?`

    Style class: `multi_option_prompt`

    ### Output

    ```
    |
    ? Title
    | Description
    |   * Option title
    |     Option description
    | > * Option title
    ```

    ### Arguments

    ### `options`

    List of options.

    Style class: `option`

    Title style class: `option_title`

    Description style class: `option_description`

    Hovered style class: `hovered`

    Selected style class: `_selected`

    ### `selection_indicator`

    Text to be displayed as a prefix before the selected options.

    Default: `*`

    Style class: `selection_indicator`

    ### `cursor`

    Text to be displayed as a prefix before the hovered option.

    Default: `>`

    Style class: `cursor`
    """

    style_classes = ["multi_option_prompt"]

    hovered_option: int = 0
    option_selected: list[bool] = [False for _ in options]

    cursor = fmt(cursor, ["cursor", *style_classes])
    selection_indicator = fmt(
        selection_indicator, ["selection_indicator", *style_classes]
    )
    line = fmt(line, ["line", *style_classes])

    def get_option_text():
        return merge_formatted_text(
            [
                merge_formatted_text(
                    [
                        cursor if i == hovered_option else fmt(" "),
                        fmt(" "),
                        selection_indicator if option_selected[i] else fmt(" "),
                        fmt(" "),
                        fmt(
                            option.title,
                            [
                                "option",
                                "option_title",
                                *(["hovered"] if i == hovered_option else []),
                                *(["_selected"] if option_selected[i] else []),
                                *style_classes,
                            ],
                        ),
                        *(
                            [
                                fmt("\n    "),
                                fmt(
                                    option.description,
                                    [
                                        "option",
                                        "option_description",
                                        *(["hovered"] if i == hovered_option else []),
                                        *(["_selected"] if option_selected[i] else []),
                                        *style_classes,
                                    ],
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

    @component_key_bindings.add("space")
    def _(event):
        option_selected[hovered_option] = not option_selected[hovered_option]

    @component_key_bindings.add("enter")
    def _(event):
        event.app.exit(
            result=[
                *(
                    [options[i].value] if selected else []
                    for i, selected in enumerate(option_selected)
                )
            ],
            style="class:confirmed",
        )

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
