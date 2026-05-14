import json
from typing import Optional

import requests
import rich_click

from lib.cli.message import error_message, info_message, success_message
from lib.cli.prompt import Option, single_option_prompt, text_prompt
from utils import (
    BaseType,
    fetch_mc_versions,
    get_latest_release,
    validate_mc_version,
    validate_path,
)

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


@rich_click.command()
@rich_click.argument(
    "path_str",
    required=False,
    help="The directory your project will be created at.",
)
@rich_click.option(
    "-y",
    "use_default",
    flag_value="y",
    help="Use default values for all options.",
)
@rich_click.option(
    "--description",
    help="What type of project you want to create.",
)
@rich_click.option(
    "--mc-version",
    "mc_version_str",
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
    path_str: str = "",
    use_default: bool = False,
    description: str = "",
    mc_version_str: str = "",
    type: Optional[BaseType] = None,
) -> None:
    """Scaffold a new project at PATH."""

    try:
        success_message(
            title="Welcome to PackSeed!",
            description="The Minecraft pack creator.",
            connect=False,
        )

        # PATH

        if not path_str:
            # no path was specified

            if use_default:
                path_str = __file__
            else:
                path_str = (
                    text_prompt(
                        title="Where do you want to create your project?",
                        description="Press enter to use the current directory.",
                    )
                    or __file__
                )

        path = validate_path(path_str)

        # TYPE

        if not type:
            if use_default:
                type = DATA_PACK_TYPE
            else:
                type = single_option_prompt(
                    title="What type of project do you want to create?",
                    options=[
                        Option(
                            value=type, title=type.title, description=type.description
                        )
                        for type in TYPES
                    ],
                )

        if type == DATA_PACK_TYPE:
            # ▄   ▗     ▄▖    ▌
            # ▌▌▀▌▜▘▀▌  ▙▌▀▌▛▘▙▘
            # ▙▘█▌▐▖█▌  ▌ █▌▙▖▛▖
            #

            # DESCRIPTION

            if not description:
                if use_default:
                    description = ""
                else:
                    description = text_prompt(
                        title="What description do you want to add to your project?",
                        description="Press enter to skip.",
                    )

            # MC VERSION

            info_message("Loading Minecraft versions...")

            try:
                mc_versions = fetch_mc_versions()
            except requests.RequestException:
                raise Exception("Failed to load Minecraft versions!")

            success_message("Done!")

            if not mc_version_str:
                # no mc version was specified

                if use_default:
                    mc_version_str = get_latest_release(mc_versions)

                mc_version_str = text_prompt(
                    title="What Minecraft version do you want to use?",
                    description="Press enter to use the latest release.",
                ) or get_latest_release(mc_versions)

            mc_version = validate_mc_version(
                mc_version_str=mc_version_str, mc_versions=mc_versions
            )

            # create files

            json.dump(
                {
                    "pack": {
                        "description": description,
                        "min_format": [mc_version.data_pack_version],
                        "max_format": [mc_version.data_pack_version],
                    }
                },
                open(path / "pack.mcmeta", "x"),
                indent=2,
            )

            success_message("Project created.")

            success_message("You're all set!")

    except KeyboardInterrupt:
        error_message("Bye!")
        exit(1)

    except Exception as e:
        error_message(e.args[0])
        exit(1)
