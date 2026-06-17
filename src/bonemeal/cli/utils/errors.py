"""Utilities for handling errors."""

import functools
import sys
from typing import TYPE_CHECKING, Any

from bonemeal.cli.components.message import error_message
from bonemeal.core.error import BoneMealError

if TYPE_CHECKING:
    from collections.abc import Callable


class UserCancelledError(BoneMealError):
    """Error raised when the user refuses to continue."""

    title = "Bye!"


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
