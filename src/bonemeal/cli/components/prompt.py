"""Functions for printing some pre-configured prompt types."""

import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING, TextIO, TypeVar, cast

from prompt_toolkit.formatted_text import AnyFormattedText, merge_formatted_text
from prompt_toolkit.key_binding import (
    KeyBindings,
    KeyBindingsBase,
    KeyPressEvent,
    merge_key_bindings,
)
from prompt_toolkit.layout import FormattedTextControl, Window
from prompt_toolkit.widgets import TextArea

from bonemeal.cli.components.component import base_component
from bonemeal.cli.components.utils import BORDER_VERTICAL, ComponentMode, LineMode, fmt

if TYPE_CHECKING:
    from prompt_toolkit.styles import BaseStyle


def text_prompt(
    title: AnyFormattedText = None,
    description: AnyFormattedText = None,
    cursor: AnyFormattedText = ">",
    icon: AnyFormattedText = "?",
    line: AnyFormattedText = BORDER_VERTICAL,
    line_mode: LineMode = LineMode.OPEN_START,
    file: TextIO = sys.stdout,
    style: BaseStyle | None = None,
    key_bindings: KeyBindingsBase | None = None,
) -> str:
    """Print a prompt with a single line text input field.

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
    """
    style_classes = ["text_prompt"]

    cursor = fmt(cursor, ["cursor", *style_classes])
    line = fmt(line, ["line", *style_classes])

    def get_line_prefix(_: int, __: int) -> AnyFormattedText:
        return merge_formatted_text([line, fmt(" "), cursor, fmt(" ")])

    input_field = TextArea(
        multiline=False,
        get_line_prefix=get_line_prefix,
        style=fmt("", ["input", *style_classes])[0][0],
    )

    component_key_bindings = KeyBindings()

    @component_key_bindings.add("enter")
    def _(event: KeyPressEvent) -> None:
        event.app.exit(result=input_field.text, style="class:confirmed")

    key_bindings = merge_key_bindings(
        [
            component_key_bindings,
            *([key_bindings] if key_bindings else []),
        ],
    )

    return cast(
        "str",
        base_component(
            content=input_field,
            title=title,
            description=description,
            icon=icon,
            line=line,
            line_mode=line_mode,
            component_mode=ComponentMode.INTERACTIVE,
            file=file,
            style=style,
            key_bindings=key_bindings,
            style_classes=style_classes,
        ),
    )


ChoiceType = TypeVar("ChoiceType")


@dataclass
class Choice[ChoiceType]:
    """Choice class used for choice prompts."""

    value: ChoiceType
    title: AnyFormattedText
    description: AnyFormattedText = None


def single_option_prompt[ChoiceType](
    options: list[Choice[ChoiceType]],
    title: AnyFormattedText = None,
    description: AnyFormattedText = None,
    default_option: int = 0,
    cursor: AnyFormattedText = ">",
    icon: AnyFormattedText = "?",
    line: AnyFormattedText = BORDER_VERTICAL,
    line_mode: LineMode = LineMode.OPEN_START,
    file: TextIO = sys.stdout,
    style: BaseStyle | None = None,
    key_bindings: KeyBindingsBase | None = None,
) -> ChoiceType:
    """Print a prompt with a list of options where only one option can be selected.

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

    def get_option_text() -> AnyFormattedText:
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
                        fmt("\n") if i != len(options) - 1 else None,
                    ],
                )
                for i, option in enumerate(options)
            ],
        )

    def get_line_prefix(_: int, __: int) -> AnyFormattedText:
        return merge_formatted_text([line, fmt(" ")])

    option_field = Window(
        FormattedTextControl(get_option_text),
        always_hide_cursor=True,
        get_line_prefix=get_line_prefix,
    )

    component_key_bindings = KeyBindings()

    @component_key_bindings.add("up")
    def _(_: KeyPressEvent) -> None:
        nonlocal hovered_option
        if hovered_option > 0:
            hovered_option -= 1

    @component_key_bindings.add("down")
    def _(_: KeyPressEvent) -> None:
        nonlocal hovered_option
        if hovered_option < len(options) - 1:
            hovered_option += 1

    @component_key_bindings.add("enter")
    def _(event: KeyPressEvent) -> None:
        event.app.exit(result=options[hovered_option].value, style="class:confirmed")

    key_bindings = merge_key_bindings(
        [
            component_key_bindings,
            *([key_bindings] if key_bindings else []),
        ],
    )

    return cast(
        "ChoiceType",
        base_component(
            content=option_field,
            title=title,
            description=description,
            icon=icon,
            line=line,
            line_mode=line_mode,
            component_mode=ComponentMode.INTERACTIVE,
            file=file,
            style=style,
            key_bindings=key_bindings,
            style_classes=style_classes,
        ),
    )


def multi_option_prompt[ChoiceType](
    options: list[Choice[ChoiceType]],
    title: AnyFormattedText = None,
    description: AnyFormattedText = None,
    cursor: AnyFormattedText = ">",
    selection_indicator: AnyFormattedText = "*",
    icon: AnyFormattedText = "?",
    line: AnyFormattedText = BORDER_VERTICAL,
    line_mode: LineMode = LineMode.OPEN_START,
    file: TextIO = sys.stdout,
    style: BaseStyle | None = None,
    key_bindings: KeyBindingsBase | None = None,
) -> ChoiceType:
    """Print a prompt with a list of options where multiple options can be selected.

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
        selection_indicator,
        ["selection_indicator", *style_classes],
    )
    line = fmt(line, ["line", *style_classes])

    def get_option_text() -> AnyFormattedText:
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
                        fmt("\n") if i != len(options) - 1 else None,
                    ],
                )
                for i, option in enumerate(options)
            ],
        )

    def get_line_prefix(_: int, __: int) -> AnyFormattedText:
        return merge_formatted_text([line, fmt(" ")])

    option_field = Window(
        FormattedTextControl(get_option_text),
        always_hide_cursor=True,
        get_line_prefix=get_line_prefix,
    )

    component_key_bindings = KeyBindings()

    @component_key_bindings.add("up")
    def _(_: KeyPressEvent) -> None:
        nonlocal hovered_option
        if hovered_option > 0:
            hovered_option -= 1

    @component_key_bindings.add("down")
    def _(_: KeyPressEvent) -> None:
        nonlocal hovered_option
        if hovered_option < len(options) - 1:
            hovered_option += 1

    @component_key_bindings.add("space")
    def _(_: KeyPressEvent) -> None:
        option_selected[hovered_option] = not option_selected[hovered_option]

    @component_key_bindings.add("enter")
    def _(event: KeyPressEvent) -> None:
        event.app.exit(
            result=[
                *(
                    [options[i].value] if selected else []
                    for i, selected in enumerate(option_selected)
                ),
            ],
            style="class:confirmed",
        )

    key_bindings = merge_key_bindings(
        [
            component_key_bindings,
            *([key_bindings] if key_bindings else []),
        ],
    )

    return cast(
        "ChoiceType",
        base_component(
            content=option_field,
            title=title,
            description=description,
            icon=icon,
            line=line,
            line_mode=line_mode,
            component_mode=ComponentMode.INTERACTIVE,
            file=file,
            style=style,
            key_bindings=key_bindings,
            style_classes=style_classes,
        ),
    )
