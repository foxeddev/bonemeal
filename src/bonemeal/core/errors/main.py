"""Base error class."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from prompt_toolkit.formatted_text import AnyFormattedText


class BoneMealError(BaseException):
    """Base error class."""

    title: AnyFormattedText
    description: AnyFormattedText = None
