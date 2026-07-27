"""Utilities related to the config type field."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, TextIO

from bonemeal.core.errors.main import BoneMealError

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclass(frozen=True, slots=True)
class ConfigType:
    """Class for config types."""

    title: str
    file: str
    write: Callable[[dict[str, Any], TextIO], None]
    description: str | None = None


class ConfigTypeNotFoundError(BoneMealError):
    """Error raised when the queried config type could not be found."""

    def __init__(self, query: str | None = None) -> None:
        """Initialize an error from an optional query string."""
        self.title = f'"{query}" is not a valid config type!'


def find_config_type(
    query: str,
    config_types: dict[str, ConfigType],
) -> ConfigType:
    """Return the first config types whose title matches the query."""
    try:
        return next(
            config_type
            for config_type in config_types.values()
            if config_type.title.lower() == query.lower()
        )

    except StopIteration as err:
        raise ConfigTypeNotFoundError(query) from err
