from typing import Any
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings


def choice(
    message: str, options: list[tuple[Any, str]], default: int = 0, cursor: str = ">"
):
    index = default

    control = FormattedTextControl(lambda: get_text())

    def get_text():
        lines = []

        lines.append(("fg:ansiblue", "?"))
        lines.append(("", f" {message}\n"))

        for i, opt in enumerate(options):
            selected = i == index
            last = i == len(options) - 1

            lines.append(("", "│ "))
            lines.append(("", f"{cursor} " if selected else " "))
            lines.append(("bold" if selected else "", opt[1]))
            lines.append(("", "\n" if not last else ""))

        return FormattedText(lines)

    def refresh():
        control.text = get_text()

    kb = KeyBindings()

    @kb.add("up")
    def _(event):
        nonlocal index
        index = (index - 1) % len(options)
        refresh()

    @kb.add("down")
    def _(event):
        nonlocal index
        index = (index + 1) % len(options)
        refresh()

    @kb.add("enter")
    def _(event):
        event.app.exit(result=options[index][0])

    @kb.add("c-c")
    def _(event):
        event.app.exit(exception=KeyboardInterrupt)

    app = Application(
        layout=Layout(Window(content=control, always_hide_cursor=True)),
        key_bindings=kb,
        full_screen=False,
    )

    return app.run()
