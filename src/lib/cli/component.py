import sys
from typing import Optional, TextIO

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

from lib.cli.base import DEFAULT_KEY_BINDINGS, DEFAULT_STYLE, BORDER_VERTICAL, fmt


def base_component(
    content: Optional[AnyContainer] = None,
    title: AnyFormattedText = None,
    description: AnyFormattedText = None,
    icon: AnyFormattedText = "*",
    line: AnyFormattedText = BORDER_VERTICAL,
    connect: bool = True,
    interactive: bool = False,
    file: TextIO = sys.stdout,
    style: Optional[BaseStyle] = None,
    key_bindings: Optional[KeyBindingsBase] = None,
    style_classes: list[str] = [],
):
    """
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

    A description to display below the component’s title.

    Style class: `description`

    #### `icon`

    Text replacing the topmost line element.

    Default: `*`

    Style class: `icon`

    #### `line`

    Text to be displayed as a border left to the component.

    Default: `|`

    Style class: `line`

    #### `connect`

    Whether to add an additional line before the component. Used to add visual connection between multiple component.

    Default: `True`

    #### `file`

    The file where the component should be printed.

    Default: `sys.stdout`

    #### `style`

    Style to apply to the whole message.

    #### `style_classes`

    Additional style classes to apply to all text fragments.
    """

    style = merge_styles([DEFAULT_STYLE, *([style] if style else [])])
    key_bindings = merge_key_bindings(
        [DEFAULT_KEY_BINDINGS, *([key_bindings] if key_bindings else [])]
    )

    title = fmt(title, ["title", *style_classes])
    description = fmt(description, ["description", *style_classes])
    icon = fmt(icon, ["icon", *style_classes])
    line = fmt(line, ["line", *style_classes])

    if connect:
        print_formatted_text(line)

    def get_line_prefix(line_number, _):
        return (
            merge_formatted_text([icon, fmt(" ")])
            if line_number == 0
            else merge_formatted_text([line, fmt(" ")])
        )

    return Application(
        Layout(
            HSplit(
                [
                    Window(
                        FormattedTextControl(
                            merge_formatted_text(
                                [
                                    *([title] if title else []),
                                    *([fmt("\n"), description] if description else []),
                                ]
                            )
                        ),
                        always_hide_cursor=True,
                        get_line_prefix=get_line_prefix,
                        wrap_lines=True,
                    ),
                    *([content] if content else []),
                ]
            )
        ),
        style=style,
        key_bindings=key_bindings if interactive else None,
        after_render=(lambda app: app.exit() if (not app.is_done) else None)
        if not interactive
        else None,
        output=create_output(file),
    ).run()
