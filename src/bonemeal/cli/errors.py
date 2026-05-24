"""Base error classes and decorator."""

import functools
import sys
from typing import TYPE_CHECKING, Any

from bonemeal.cli.components.message import error_message

if TYPE_CHECKING:
    from collections.abc import Callable

    from prompt_toolkit.formatted_text import AnyFormattedText


class BoneMealError(BaseException):
    """The base error class for the CLI."""

    title: AnyFormattedText
    description: AnyFormattedText = None


class UserCancelledError(BoneMealError):
    """Error raised when the user refuses to continue."""

    title: AnyFormattedText = "Bye!"


def handle_errors(func: Callable[..., Any]) -> Callable[..., Any]:
    """Nicely exit on errors."""

    @functools.wraps(func)
    def wrapper(*args: ..., **kwargs: ...) -> Callable[..., Any]:
        try:
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt as err:
                raise UserCancelledError from err
        except BoneMealError as err:
            error_message(err.title, err.description)
            sys.exit(1)

    return wrapper
