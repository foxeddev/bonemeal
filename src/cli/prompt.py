from typing import Optional

from prompt_toolkit import HTML
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout, VSplit, Window, HSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import AnyFormattedText


def prompt(
    message: AnyFormattedText,
    default: str = "",
    instructions: Optional[AnyFormattedText] = None,
    symbol: AnyFormattedText = HTML("<ansiblue>?</ansiblue>"),
    line: str = "│",
    cursor: AnyFormattedText = ">",
):
    input_field = TextArea(text=default, multiline=False)

    border = HSplit(
        [
            Window(
                content=FormattedTextControl(text=symbol),
                dont_extend_width=True,
                dont_extend_height=True,
                always_hide_cursor=True,
            ),
            Window(char=line, height=2 if instructions else 1),
        ]
    )

    content = HSplit([])
    content.children.append(
        Window(
            content=FormattedTextControl(text=message),
            dont_extend_height=True,
        )
    )
    if instructions:
        content.children.append(
            Window(
                content=FormattedTextControl(text=instructions),
                dont_extend_height=True,
            )
        )
    content.children.append(
        VSplit(
            [
                Window(
                    content=FormattedTextControl(text=cursor),
                    dont_extend_width=True,
                    dont_extend_height=True,
                ),
                input_field,
            ],
            padding=1,
        )
    )

    root_container = VSplit([border, content], padding=1)
    layout = Layout(root_container)

    kb = KeyBindings()

    @kb.add("enter")
    def _(event):
        event.app.exit(result=input_field.text)

    @kb.add("c-c")
    def _(event):
        event.app.exit(exception=KeyboardInterrupt)

    app = Application(layout=layout, key_bindings=kb)
    return app.run()
