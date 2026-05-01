from typing import Optional

from prompt_toolkit import Application
from prompt_toolkit.layout import (
    AnyContainer,
    HSplit,
    Layout,
    UIControl,
    VSplit,
    Window,
    Container,
)
from prompt_toolkit.formatted_text import AnyFormattedText, merge_formatted_text
from prompt_toolkit.key_binding import KeyBindingsBase, merge_key_bindings
from prompt_toolkit.styles import BaseStyle, Style, merge_styles

from lib.cli.base import Border


__all__ = [
    "Question",
]


class FlexWindow(Window):
    def __init__(self, content: UIControl):
        super().__init__(
            content=content,
            dont_extend_width=True,
            dont_extend_height=True,
            always_hide_cursor=True,
        )


def border(
    line_height: int,
    icon: AnyFormattedText = "*",
    line_char: AnyFormattedText = Border.VERTICAL,
):
    return (
        merge_formatted_text(
            [
                icon if line_height > 1 else None,
                *(
                    merge_formatted_text([line_char, "\n"])
                    for _ in range(line_height - 2)
                ),
                line_char if line_height > 2 else None,
            ]
        )
        or None
    )


class Question(Application):
    icon: AnyFormattedText
    line_char: AnyFormattedText
    title: AnyFormattedText
    description: AnyFormattedText
    actions: Optional[Container]
    style: BaseStyle
    key_bindings: KeyBindingsBase

    def __init__(
        self,
        icon: AnyFormattedText = None,
        line_char: AnyFormattedText = None,
        title: AnyFormattedText = None,
        description: AnyFormattedText = None,
        actions: Optional[Container] = None,
        style: Optional[BaseStyle] = None,
        key_bindings: Optional[KeyBindingsBase] = None,
    ):
        self.icon = icon
        self.line_char = line_char
        self.title = title
        self.description = description
        self.actions = actions
        self.style = default_style
        if style:
            self.style = merge_styles([self.style, style])
        self.key_bindings = default_key_bindings
        if key_bindings:
            merge_key_bindings([self.key_bindings, key_bindings])

        border = self._get_border()
        container = self._get_content()

        container_content = []
        if border:
            container_content.append(border)
        if container_content:
            container_content.append(container)

        super().__init__(
            layout=Layout(
                container=VSplit(
                    container_content,
                    padding=1,
                )
            )
            if container_content
            else None,
            style=self.style,
            key_bindings=merge_key_bindings(
                [
                    default_key_bindings,
                    self.key_bindings,
                ]
            ),
        )

    def ask(self):
        try:
            self.run()
        except KeyboardInterrupt:
            ErrorMessage(message="Operation cancelled.").print()
            exit()

    def _get_border(self):
        container = self._get_content()

        return (
            Border(
                line_height=container.preferred_height(1, -1).preferred,
                icon=self.icon,
                line_char=self.line_char,
            )
            if container
            else None
        )

    def _get_content(self):
        content: list[AnyContainer] = []

        if self.title:
            content.append(Title(self.title))
        if self.description:
            content.append(Description(self.description))
        if self.actions:
            content.append(self.actions)

        return HSplit(content) if content else None


class ErrorMessage(Message):
    def __init__(self, message):
        super().__init__(message=message, icon="!", style=Style([("icon", "ansired")]))


Message(message="hello").print()
