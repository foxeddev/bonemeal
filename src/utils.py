"""Utilities for the CLI."""

import enum
import shutil
import subprocess
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING

import requests
from send2trash import send2trash

from lib.cli.message import info_message, success_message, warning_message
from lib.cli.prompt import Option, single_option_prompt

if TYPE_CHECKING:
    from prompt_toolkit.formatted_text import AnyFormattedText


@dataclass(frozen=True, slots=True)
class PackSeedError(BaseException):
    """The base error class for the CLI."""

    title: AnyFormattedText
    description: AnyFormattedText = None


@dataclass(frozen=True, slots=True)
class UserCancelled(BaseException):
    """Error thrown when the user refuses to continue."""

    title: AnyFormattedText = "Bye!"


@dataclass(frozen=True, slots=True)
class BaseProjectType:
    """The base class for project types."""

    id: str
    option_id: str
    title: AnyFormattedText
    description: AnyFormattedText = None


class MCVersionType(enum.StrEnum):
    """Whether the Minecraft version is a release or a snapshot."""

    RELEASE = "release"
    SNAPSHOT = "snapshot"


@dataclass(frozen=True, slots=True)
class MCVersion:
    """Class representing a Minecraft version."""

    id: str
    name: str
    type: MCVersionType
    data_pack_version: tuple[int, int]
    resource_pack_version: tuple[int, int]


class FetchMCVersionError(PackSeedError):
    """Error thrown when Minecraft versions couldn't be loaded from GitHub."""

    title: AnyFormattedText
    description: AnyFormattedText = None

    def __init__(self, response: requests.Response | None) -> None:
        """Initialize an error from an optional response object."""
        self.title = "Failed to fetch Minecraft versions!"
        self.description = (
            f"{response.status_code} {response.reason}" if response else None
        )


@cache
def fetch_mc_versions() -> list[MCVersion]:
    """Load a list of all Minecraft versions from GitHub."""
    info_message("Loading Minecraft versions...")

    try:
        response = requests.get(
            "https://raw.githubusercontent.com/misode/mcmeta/summary/versions/data.json",
            timeout=5,
        )

        response.raise_for_status()

        success_message("Done!")

        return [
            MCVersion(
                id=version["id"],
                name=version["name"],
                type=version["type"],
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


@dataclass(frozen=True, slots=True)
class NoMCReleaseError(PackSeedError):
    """Error thrown when no Minecraft release was found."""

    title: AnyFormattedText = "No Minecraft release was found!"


@cache
def get_latest_release() -> str:
    """Get the ID of the latest Minecraft release."""
    releases = [
        mc_version
        for mc_version in fetch_mc_versions()
        if mc_version.type == MCVersionType.RELEASE
    ]

    if len(releases) == 0:
        # no release found

        raise NoMCReleaseError

    return releases[0].id


def get_git_username() -> str | None:
    """Try to find the user's Git username or return None."""
    try:
        git_path = shutil.which("git")

        if not git_path:
            return None

        return subprocess.check_output(  # noqa: S603
            [git_path, "config", "user.name"],
            text=True,
        ).strip()

    except subprocess.CalledProcessError:
        return None


def validate_path(path: Path) -> Path:
    """Check if a path is valid for project creation."""
    if path.is_dir(follow_symlinks=False):
        # path is a directory

        if any(path.iterdir()):
            # path contains files

            warning_message("The specified directory is not empty!")
        else:
            return path

    elif path.exists():
        # path exists, but is not a directory

        warning_message("A file with the specified name already exists!")
    else:
        # path doesn't exist

        path.mkdir(parents=True)
        return path

    if not single_option_prompt(
        title="Do you want to overwrite it?",
        options=[
            Option(value=True, title="OK"),
            Option(value=False, title="Cancel"),
        ],
        default_option=1,
    ):
        # user declines to overwrite

        raise UserCancelled

    # user accepts to overwrite

    send2trash(path)
    path.mkdir(exist_ok=True, parents=True)
    return path


class InvalidMCVersionError(PackSeedError):
    """Error thrown when the provided Minecraft version is invalid."""

    title: AnyFormattedText
    description: AnyFormattedText = None

    def __init__(self, mc_version_str: str) -> None:
        """Initialize an error from the invalid Minecraft version string object."""
        self.title = f'"{mc_version_str}" is not a valid Minecraft version!'


def validate_mc_version(mc_version_str: str) -> MCVersion:
    """Check if a Minecraft version is valid."""
    # find all matching versions
    mc_versions = [
        mc_version
        for mc_version in fetch_mc_versions()
        if mc_version.id.lower() == mc_version_str.lower()
        or mc_version.name.lower() == mc_version_str.lower()
    ]

    if len(mc_versions) == 0:
        # no matching versions found

        raise InvalidMCVersionError(mc_version_str=mc_version_str)
    if len(mc_versions) > 1:
        # multiple matching versions found

        warning_message("Found multiple versions with the same ID!")

    return mc_versions[0]


class PromptMode(enum.Enum):
    """Whether to show prompts to the user or always use default values."""

    SHOW_PROMPTS = "show_prompts"
    USE_DEFAULT = "use_default"
