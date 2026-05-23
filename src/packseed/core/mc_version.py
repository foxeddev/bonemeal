"""Classes and helpers related to Minecraft versions."""

import enum
from dataclasses import dataclass
from functools import cache

import requests

from packseed.cli.errors import PackSeedError


class MCVersionType(enum.Enum):
    """Whether the Minecraft version is a release or a snapshot."""

    RELEASE = enum.auto()
    SNAPSHOT = enum.auto()


@dataclass(frozen=True, slots=True)
class MCVersion:
    """Class representing a Minecraft version."""

    id: str
    name: str
    type: MCVersionType
    data_pack_version: tuple[int, int]
    resource_pack_version: tuple[int, int]


class FetchMCVersionError(PackSeedError):
    """Error raised when Minecraft versions couldn't be fetched from GitHub."""

    def __init__(self, response: requests.Response | None = None) -> None:
        """Initialize an error from an optional response object."""
        self.title = "Failed to fetch Minecraft versions!"
        self.description = (
            f"{response.status_code} {response.reason}" if response else None
        )


@cache
def fetch_mc_versions() -> list[MCVersion]:
    """Fetch a list of current Minecraft versions from GitHub."""
    try:
        response = requests.get(
            "https://raw.githubusercontent.com/misode/mcmeta/summary/versions/data.json",
            timeout=5,
        )

        response.raise_for_status()

        return [
            MCVersion(
                id=version["id"],
                name=version["name"],
                type=MCVersionType.RELEASE
                if version["type"] == "release"
                else MCVersionType.SNAPSHOT,
                data_pack_version=(
                    version["data_pack_version"],
                    version["data_pack_version_minor"],
                ),
                resource_pack_version=(
                    version["resource_pack_version"],
                    version["resource_pack_version_minor"],
                ),
            )
            for version in response.json()
        ]

    except requests.RequestException as err:
        raise FetchMCVersionError(err.response) from err


class NoMCReleaseError(PackSeedError):
    """Error raised when no Minecraft release was found."""

    title = "No Minecraft release was found!"


@cache
def get_latest_mc_release() -> MCVersion:
    """Fetch the latest Minecraft release from GitHub."""
    releases = [
        mc_version
        for mc_version in fetch_mc_versions()
        if mc_version.type == MCVersionType.RELEASE
    ]

    if len(releases) > 0:
        return releases[0]

    raise NoMCReleaseError


class MCVersionNotFoundError(PackSeedError):
    """Error raised when the provided Minecraft version could not be found."""

    def __init__(self, query: str | None = None) -> None:
        """Initialize an error from an optional query string."""
        self.title = f'"{query}" is not a valid Minecraft version!'


def find_mc_version(query: str) -> MCVersion:
    """Return the first Minecraft version whose ID or name match the query."""
    mc_versions = [
        mc_version
        for mc_version in fetch_mc_versions()
        if mc_version.id.lower() == query.lower()
        or mc_version.name.lower() == query.lower()
    ]

    if len(mc_versions) > 0:
        return mc_versions[0]

    raise MCVersionNotFoundError
