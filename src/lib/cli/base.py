from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings


BORDER_VERTICAL = "\u2502"


DEFAULT_STYLE = Style(
    [
        ("details", "ansigray"),
        ("icon", "bold"),
        ("icon info", "ansiblue"),
        ("icon success", "ansigreen"),
        ("icon warning", "ansiyellow"),
        ("icon error", "ansired"),
    ]
)


DEFAULT_KEY_BINDINGS = KeyBindings()


@DEFAULT_KEY_BINDINGS.add("c-c")
def _(event):
    event.app.exit(exception=KeyboardInterrupt)
