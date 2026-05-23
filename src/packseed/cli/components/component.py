"""Function for printing a `base_component`."""

import sys
from typing import TextIO, cast

from prompt_toolkit import Application, print_formatted_text
from prompt_toolkit.formatted_text import AnyFormattedText, merge_formatted_text
from prompt_toolkit.key_binding import KeyBindingsBase, merge_key_bindings
from prompt_toolkit.layout import (
    AnyContainer,
    FormattedTextControl,
    HSplit,
    Layout,
    Window,
)
from prompt_toolkit.output import create_output
from prompt_toolkit.styles import BaseStyle, merge_styles

from packseed.cli.components.utils import (
    BORDER_VERTICAL,
    DEFAULT_KEY_BINDINGS,
    DEFAULT_STYLE,
    ComponentMode,
    LineMode,
    fmt,
)


def base_component(
    content: AnyContainer | None = None,
    title: AnyFormattedText = None,
    description: AnyFormattedText = None,
    icon: AnyFormattedText = "*",
    line: AnyFormattedText = BORDER_VERTICAL,
    line_mode: LineMode = LineMode.OPEN_START,
    component_mode: ComponentMode = ComponentMode.INTERACTIVE,
    file: TextIO = sys.stdout,
    style: BaseStyle | None = None,
    key_bindings: KeyBindingsBase | None = None,
    style_classes: list[str] | None = None,
) -> object:
    """Print a formatted component.

    ### Output

    ```
    |
    * Title
    | Description
    Content
    ```

    ### Arguments

    #### `content`

    A container to display below the component.

    #### `title`

    The title of the component.

    Style class: `title`

    #### `description`

    A description to display below the component's title.

    Style class: `description`

    #### `icon`

    Text replacing the topmost line element.

    Default: `*`

    Style class: `icon`

    #### `line`

    Text to be displayed as a border left to the component.

    Default: `|`

    Style class: `line`

    #### `line_mode`

    Whether an additional line should be added before the component.

    Used to add visual connection between multiple components.

    Default: `ComponentMode.INTERACTIVE`

    #### `component_mode`

    Whether the component should automatically exit after printing or stay interactive.

    Default: `LineMode.OPEN_START`

    #### `file`

    The file where the component should be printed.

    Default: `sys.stdout`

    #### `style`

    Style to apply to the whole message.

    #### `style_classes`

    Additional style classes to apply to all text fragments.
    """
    if style_classes is None:
        style_classes = []
    style = merge_styles([DEFAULT_STYLE, *([style] if style else [])])
    key_bindings = merge_key_bindings(
        [DEFAULT_KEY_BINDINGS, *([key_bindings] if key_bindings else [])],
    )

    title = fmt(title, ["title", *style_classes])
    description = fmt(description, ["description", *style_classes])
    icon = fmt(icon, ["icon", *style_classes])
    line = fmt(line, ["line", *style_classes])

    if line_mode == LineMode.OPEN_START:
        print_formatted_text(line)

    def get_line_prefix(line_number: int, _: int) -> AnyFormattedText:
        return (
            merge_formatted_text(
                [icon if line_number == 0 and icon else line, fmt(" ")],
            )
            if line
            else None
        )

    return cast(
        "object",
        Application(
            Layout(
                HSplit(
                    [
                        Window(
                            FormattedTextControl(
                                merge_formatted_text(
                                    [
                                        *([title] if title else []),
                                        *(
                                            [fmt("\n"), description]
                                            if description
                                            else []
                                        ),
                                    ],
                                ),
                            ),
                            always_hide_cursor=True,
                            get_line_prefix=get_line_prefix,
                            wrap_lines=True,
                        ),
                        *([content] if content else []),
                    ],
                ),
            ),
            style=style,
            key_bindings=key_bindings
            if component_mode is ComponentMode.INTERACTIVE
            else None,
            after_render=(lambda app: app.exit() if (not app.is_done) else None)
            if component_mode is ComponentMode.AUTO_EXIT
            else None,
            output=create_output(file),
        ).run(),
    )
