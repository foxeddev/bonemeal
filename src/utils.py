import enum
from dataclasses import dataclass
from pathlib import Path

import requests
from prompt_toolkit.formatted_text import AnyFormattedText
from send2trash import send2trash

from lib.cli.message import warning_message
from lib.cli.prompt import Option, single_option_prompt


@dataclass(frozen=True, slots=True)
class BaseType:
    id: str
    option_id: str
    title: AnyFormattedText
    description: AnyFormattedText = None


class MCVersionType(enum.StrEnum):
    RELEASE = "release"
    SNAPSHOT = "snapshot"


@dataclass(frozen=True, slots=True)
class MCVersion:
    id: str
    name: str
    type: MCVersionType
    data_pack_version: tuple[int, int]
    resource_pack_version: tuple[int, int]


def fetch_mc_versions() -> list[MCVersion]:
    response = requests.get(
        "https://raw.githubusercontent.com/misode/mcmeta/summary/versions/data.json",
        timeout=5,
    )

    response.raise_for_status()

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


def get_latest_release(mc_versions: list[MCVersion]) -> str:
    releases = [
        version for version in mc_versions if version.type == MCVersionType.RELEASE
    ]
    if len(releases) == 0:
        raise Exception("There is no Minecraft release, for some reason...")
    else:
        return releases[0].id


def validate_path(path_str: str) -> Path:
    path = Path(path_str)

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

        exit(1)
    else:
        # user accepts to overwrite

        send2trash(path)
        path.mkdir(exist_ok=True, parents=True)

    return path


def validate_mc_version(mc_version_str: str, mc_versions: list[MCVersion]) -> MCVersion:
    # find all matching versions
    mc_versions = [
        mc_version
        for mc_version in mc_versions
        if mc_version.id.lower() is mc_version_str.lower()
    ]

    if len(mc_versions) == 0:
        # no matching versions found

        raise Exception(f'"{mc_version_str}" is not a valid Minecraft version!')

    return mc_versions[0]
