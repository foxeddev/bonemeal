"""Utilities related to the Minecraft version field."""

import enum
from dataclasses import dataclass
from functools import cache
from typing import Any

import requests

from bonemeal.core.errors.main import BoneMealError


class MCVersionType(enum.Enum):
    """Whether the Minecraft version is a release or a snapshot."""

    RELEASE = "release"
    SNAPSHOT = "snapshot"


@dataclass(frozen=True, order=True)
class MCVersion:
    """Class representing a Minecraft version."""

    order_index: int

    id: str
    name: str
    type: MCVersionType
    data_pack_version: tuple[int, int]
    resource_pack_version: tuple[int, int]


class ParseMCVersionsError(BoneMealError):
    """Error raised when Minecraft versions couldn't be parsed."""

    title = "Failed to parse Minecraft versions!"


def parse_mc_versions(mc_versions: list[Any]) -> dict[str, MCVersion]:
    """Convert a Minecraft version list to a list of MCVersion instances."""
    try:
        return {
            version["id"]: MCVersion(
                order_index=i,
                id=version["id"],
                name=version["name"],
                type=MCVersionType(version["type"]),
                data_pack_version=(
                    version["data_pack_version"],
                    version["data_pack_version_minor"],
                ),
                resource_pack_version=(
                    version["resource_pack_version"],
                    version["resource_pack_version_minor"],
                ),
            )
            for i, version in enumerate(mc_versions)
        }
    except (KeyError, ValueError, TypeError) as err:
        raise ParseMCVersionsError from err


class FetchMCVersionsError(BoneMealError):
    """Error raised when Minecraft versions couldn't be fetched from GitHub."""

    title = "Failed to fetch Minecraft versions!"

    def __init__(self, response: requests.Response | None = None) -> None:
        """Initialize an error from an optional response object."""
        self.description = (
            f"{response.status_code} {response.reason}" if response else None
        )


@cache
def fetch_mc_versions() -> dict[str, MCVersion]:
    """Fetch a list of current Minecraft versions from GitHub."""
    try:
        response = requests.get(
            "https://raw.githubusercontent.com/misode/mcmeta/summary/versions/data.json",
            timeout=5,
        )
        response.raise_for_status()
        return parse_mc_versions(response.json())

    except requests.RequestException as err:
        raise FetchMCVersionsError(err.response) from err


class NoMCReleaseError(BoneMealError):
    """Error raised when no Minecraft release was found."""

    title = "No Minecraft release was found!"


@cache
def get_latest_mc_release() -> MCVersion:
    """Fetch the latest Minecraft release from GitHub."""
    try:
        return next(
            mc_version
            for mc_version in fetch_mc_versions().values()
            if mc_version.type == MCVersionType.RELEASE
        )

    except StopIteration as err:
        raise NoMCReleaseError from err


class MCVersionNotFoundError(BoneMealError):
    """Error raised when the queried Minecraft version could not be found."""

    def __init__(self, query: str | None = None) -> None:
        """Initialize an error from an optional query string."""
        self.title = f'"{query}" is not a valid Minecraft version!'


def find_mc_version(query: str) -> MCVersion:
    """Return the first Minecraft version whose ID or name match the query."""
    query = query.lower()

    try:
        return next(
            mc_version
            for mc_version in fetch_mc_versions().values()
            if mc_version.id.lower() == query or mc_version.name.lower() == query
        )

    except StopIteration as err:
        raise MCVersionNotFoundError(query) from err
