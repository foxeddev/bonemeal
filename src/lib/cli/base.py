from typing import Optional

from prompt_toolkit.formatted_text import AnyFormattedText, to_formatted_text
from prompt_toolkit.styles import BaseStyle, Style
from prompt_toolkit.key_binding import KeyBindings


__all__ = [
    "BORDER_VERTICAL",
    "DEFAULT_STYLE",
    "DEFAULT_KEY_BINDINGS",
    "merge_style_strings",
    "fmt",
]


BORDER_VERTICAL = "\u2502"


DEFAULT_STYLE: BaseStyle = Style(
    [
        ("description", "dim"),
        ("icon", "bold"),
        ("icon info_message", "ansiblue"),
        ("icon success_message", "ansigreen"),
        ("icon warning_message", "ansiyellow"),
        ("icon error_message", "ansired"),
        ("icon text_prompt", "ansiblue"),
        ("icon option_prompt", "ansiblue"),
        ("option_description", "dim"),
    ]
)


DEFAULT_KEY_BINDINGS = KeyBindings()


@DEFAULT_KEY_BINDINGS.add("c-c")
def _(event):
    event.app.exit(exception=KeyboardInterrupt)


def merge_style_strings(styles: list[str]):
    return " ".join(style for style in styles)


def fmt(text: AnyFormattedText, classes: Optional[str | list[str]] = None):
    return (
        to_formatted_text(
            text, style=(merge_style_strings([f"class:{cls}" for cls in classes]))
        )
        if classes
        else to_formatted_text(text)
    )
