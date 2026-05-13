from dataclasses import dataclass
from typing import Optional
from prompt_toolkit.formatted_text import AnyFormattedText
import requests
import json
from pathlib import Path

from prompt_toolkit import HTML
from send2trash import send2trash

from lib.cli.message import error_message, info_message, success_message

from lib.cli.prompt import (
    Option,
    single_option_prompt,
    text_prompt,
)
import rich_click


@dataclass(frozen=True, slots=True)
class BaseType:
    id: str
    option_id: str
    title: AnyFormattedText
    description: AnyFormattedText = None


DATA_PACK_TYPE = BaseType(
    id="data_pack",
    option_id="data-pack",
    title="Data Pack",
)
RESOURCE_PACK_TYPE = BaseType(
    id="resource_pack",
    option_id="resource-pack",
    title="Resource Pack",
)
BEET_PROJECT_TYPE = BaseType(
    id="beet_project",
    option_id="beet-project",
    title="Beet Project",
    description="Beet is a Minecraft pack development kit for both data packs and resource packs.",
)

TYPES = [DATA_PACK_TYPE, RESOURCE_PACK_TYPE, BEET_PROJECT_TYPE]


@dataclass(frozen=True, slots=True)
class MCVersion:
    id: str
    name: str
    type: str  # release / snapshot
    data_pack_version: tuple[int, int]
    resource_pack_version: tuple[int, int]


def fetch_mc_versions():
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


def create_data_pack(
    path: Path,
    mc_version_string: Optional[str] = None,
    description: Optional[str] = None,
):
    path.mkdir(exist_ok=True, parents=True)

    info_message("Loading Minecraft versions...")

    try:
        MC_VERSIONS = fetch_mc_versions()
    except requests.RequestException:
        raise Exception("Failed to load Minecraft versions!")

    success_message("Done!")

    if not mc_version_string:
        mc_version_string = text_prompt(
            title="What Minecraft version do you want to use?",
            description="Press enter to use the latest release.",
        )

    if not mc_version_string:
        mc_version = [version for version in MC_VERSIONS if version.type == "release"]
        if len(mc_version) == 0:
            raise Exception("There is no latest Minecraft version, for some reason...")
        else:
            mc_version = mc_version[0]
    else:
        mc_version = [
            version for version in MC_VERSIONS if version.name == mc_version_string
        ]
        if len(mc_version) == 0:
            raise Exception(f'"{mc_version_string}" is not a valid Minecraft version!')
        else:
            mc_version = mc_version[0]

    if not description:
        description = text_prompt(
            title="What description do you want to add to your project?",
            description="Press enter to skip.",
        )

    with open(path / "pack.mcmeta", "x") as f:
        json.dump(
            {
                "pack": {
                    "description": description,
                    "min_format": [mc_version.data_pack_version],
                    "max_format": [mc_version.data_pack_version],
                }
            },
            f,
            indent=2,
        )


@rich_click.command()
@rich_click.argument(
    "path",
    type=str,
    required=False,
    help="The directory your project will be created at.",
)
@rich_click.option(
    "--description",
    type=str,
    help="What type of project you want to create.",
)
@rich_click.option(
    "--mc-version",
    type=str,
    help="What Minecraft version you want to use.",
)
@rich_click.option(
    "--type",
    type=rich_click.Choice(
        choices=[type.option_id for type in TYPES], case_sensitive=False
    ),
    help="What type of project you want to create.",
)
def create(
    path: Optional[str] = None,
    mc_version: Optional[str] = None,
    description: Optional[str] = None,
    type: Optional[BaseType] = None,
) -> None:
    """Scaffold a new project at PATH."""

    success_message(
        title="Welcome to PackSeed!",
        description="The Minecraft pack creator.",
        connect=False,
    )

    path = path.strip() if path else ""

    try:
        if not path:
            path = text_prompt(
                title="Where do you want to create your project?",
                description="Press enter to use the current directory.",
            )

        path = path.strip() if path else ""

        full_path = Path(path).resolve()

        if full_path.is_dir(follow_symlinks=False):
            if any(full_path.iterdir()):
                if not single_option_prompt(
                    title="The specified directory is not empty. Do you want to overwrite it?",
                    options=[
                        Option(value=True, title="OK"),
                        Option(value=False, title="Cancel"),
                    ],
                    default_option=1,
                    icon=HTML("<ansiyellow>!</ansiyellow>"),
                ):
                    exit(0)
                else:
                    send2trash(full_path)

        elif full_path.exists():
            if not single_option_prompt(
                title="A file with the specified name already exists. Do you want to overwrite it?",
                options=[
                    Option(value=True, title="OK"),
                    Option(value=False, title="Cancel"),
                ],
                default_option=1,
                icon=HTML("<ansiyellow>!</ansiyellow>"),
            ):
                exit(0)
            else:
                send2trash(full_path)

        type = (
            [loop_type for loop_type in TYPES if loop_type.option_id is type][0]
            if type
            else None
        )

        if not type:
            type = single_option_prompt(
                title="What type of project do you want to create?",
                options=[
                    Option(value=type, title=type.title, description=type.description)
                    for type in TYPES
                ],
            )

        if type == DATA_PACK_TYPE:
            create_data_pack(
                path=full_path, mc_version_string=mc_version, description=description
            )

    except Exception as e:
        error_message(e.args[0])
        exit(1)

    success_message("Project created.")

    success_message("You're all set!")
