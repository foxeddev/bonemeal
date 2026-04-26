from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout, VSplit, Window, HSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.formatted_text import AnyFormattedText


def print(message: AnyFormattedText):
    root_lines = []

    root_lines.append(
        VSplit(
            [
                Window(char="* ", dont_extend_width=True),
                Window(
                    content=FormattedTextControl(text=message), dont_extend_width=True
                ),
            ]
        )
    )

    root_container = HSplit(root_lines)
    layout = Layout(root_container)

    app = Application(layout=layout)
    return app.run()
