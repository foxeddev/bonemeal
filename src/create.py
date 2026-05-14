import json
from pathlib import Path
from typing import Optional

import rich_click

from lib.cli.message import error_message, info_message, success_message
from lib.cli.prompt import Option, single_option_prompt, text_prompt
from utils import (
    BaseType,
    PackSeedException,
    fetch_mc_versions,
    get_git_username,
    get_latest_release,
    validate_mc_version,
    validate_path,
)

DATA_PACK_TYPE = BaseType(
    id="data_pack",
    option_id="data-pack",
    title="Data pack",
)
RESOURCE_PACK_TYPE = BaseType(
    id="resource_pack",
    option_id="resource-pack",
    title="Resource pack",
)
BEET_PROJECT_TYPE = BaseType(
    id="beet_project",
    option_id="beet-project",
    title="Beet project",
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
    help="What description you want to add to your project.",
)
@rich_click.option(
    "--author",
    help="What author you want to set for your project.",
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
    path_str: Optional[str] = None,
    use_default: bool = False,
    description: Optional[str] = None,
    author: Optional[str] = None,
    mc_version_str: Optional[str] = None,
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

        id = path.name

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
            # ▄   ▗           ▌
            # ▌▌▀▌▜▘▀▌  ▛▌▀▌▛▘▙▘
            # ▙▘█▌▐▖█▌  ▙▌█▌▙▖▛▖
            #           ▌

            # DESCRIPTION

            if not description:
                if use_default:
                    description = ""
                else:
                    description = text_prompt(
                        title="What description do you want to add to your data pack?",
                        description="Press enter to skip.",
                    )

            # MC VERSION

            info_message("Loading Minecraft versions...")

            mc_versions = fetch_mc_versions()

            success_message("Done!")

            if not mc_version_str:
                latest_release = get_latest_release(mc_versions)

                if use_default:
                    mc_version_str = latest_release

                mc_version_str = (
                    text_prompt(
                        title="What Minecraft version do you want to use?",
                        description="Press enter to use the latest release.",
                    )
                    or latest_release
                )

            mc_version = validate_mc_version(
                mc_version_str=mc_version_str, mc_versions=mc_versions
            )

            # create files

            with open(path / "pack.mcmeta", "x") as f:
                json.dump(
                    {
                        "pack": {
                            "description": description,
                            "min_format": [mc_version.data_pack_version],
                            "max_format": [mc_version.data_pack_version],
                        }
                    },
                    fp=f,
                    indent=2,
                )

            success_message("Data pack created.")

        if type == RESOURCE_PACK_TYPE:
            # ▄▖                      ▌
            # ▙▘█▌▛▘▛▌▌▌▛▘▛▘█▌  ▛▌▀▌▛▘▙▘
            # ▌▌▙▖▄▌▙▌▙▌▌ ▙▖▙▖  ▙▌█▌▙▖▛▖
            #                   ▌

            # DESCRIPTION

            if not description:
                if use_default:
                    description = ""
                else:
                    description = text_prompt(
                        title="What description do you want to add to your resource pack?",
                        description="Press enter to skip.",
                    )

            # MC VERSION

            info_message("Loading Minecraft versions...")

            mc_versions = fetch_mc_versions()

            success_message("Done!")

            if not mc_version_str:
                latest_release = get_latest_release(mc_versions)

                if use_default:
                    mc_version_str = latest_release

                mc_version_str = (
                    text_prompt(
                        title="What Minecraft version do you want to use?",
                        description="Press enter to use the latest release.",
                    )
                    or latest_release
                )

            mc_version = validate_mc_version(
                mc_version_str=mc_version_str, mc_versions=mc_versions
            )

            # create files

            with open(path / "pack.mcmeta", "x") as f:
                json.dump(
                    {
                        "pack": {
                            "description": description,
                            "min_format": [mc_version.resource_pack_version],
                            "max_format": [mc_version.resource_pack_version],
                        }
                    },
                    fp=f,
                    indent=2,
                )

            success_message("Resource pack created.")

        if type == BEET_PROJECT_TYPE:
            # ▄     ▗          ▘    ▗
            # ▙▘█▌█▌▜▘  ▛▌▛▘▛▌ ▌█▌▛▘▜▘
            # ▙▘▙▖▙▖▐▖  ▙▌▌ ▙▌ ▌▙▖▙▖▐▖
            #           ▌     ▙▌

            # DESCRIPTION

            if not description:
                if use_default:
                    description = ""
                else:
                    description = text_prompt(
                        title="What description do you want to add to your Beet project?",
                        description="Press enter to skip.",
                    )

            if not author:
                git_username = get_git_username()

                if use_default:
                    author = git_username
                else:
                    author = (
                        text_prompt(
                            title="What author do you want to set to your Beet project?",
                            description="Press enter to use your Git username."
                            if git_username
                            else "Press enter to skip.",
                        )
                        or git_username
                    )

            # MC VERSION

            info_message("Loading Minecraft versions...")

            mc_versions = fetch_mc_versions()

            success_message("Done!")

            if not mc_version_str:
                latest_release = get_latest_release(mc_versions)

                if use_default:
                    mc_version_str = latest_release

                mc_version_str = (
                    text_prompt(
                        title="What Minecraft version do you want to use?",
                        description="Press enter to use the latest release.",
                    )
                    or latest_release
                )

            mc_version = validate_mc_version(
                mc_version_str=mc_version_str, mc_versions=mc_versions
            )

            # create files

            with open(path / "beet.json", "x") as f:
                json.dump(
                    {
                        "id": id,
                        "name": id,
                        "version": "0.1.0",
                        "description": description,
                        "author": author,
                        "minecraft": mc_version.id,  # TODO fix mc version for Beet
                        "output": "build",
                        "data_pack": {"load": ["src"]},
                        "resource_pack": {"load": ["src"]},
                    },
                    fp=f,
                    indent=2,
                )

            Path(path / "data" / id).mkdir(parents=True)
            Path(path / "assets" / id).mkdir(parents=True)

            success_message("Beet project created.")

    except KeyboardInterrupt:
        error_message("Bye!")
        exit(1)

    except PackSeedException as e:
        error_message(e.title, e.description)
        exit(1)
