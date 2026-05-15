"""The CLI command used for scaffolding a new project."""

import json
import sys
from pathlib import Path

import rich_click

from lib.cli.message import error_message, success_message
from lib.cli.prompt import Option, single_option_prompt, text_prompt
from lib.cli.utils import LineMode
from utils import (
    BaseProjectType,
    MCVersion,
    PackSeedError,
    PromptMode,
    fetch_mc_versions,
    get_git_username,
    get_latest_release,
    validate_mc_version,
    validate_path,
)

DATA_PACK_TYPE = BaseProjectType(
    id="data_pack",
    option_id="data-pack",
    title="Data pack",
)
RESOURCE_PACK_TYPE = BaseProjectType(
    id="resource_pack",
    option_id="resource-pack",
    title="Resource pack",
)
BEET_PROJECT_TYPE = BaseProjectType(
    id="beet_project",
    option_id="beet-project",
    title="Beet project",
    description="""Beet is a Minecraft pack development kit for both data packs and \
resource packs.""",
)


PROJECT_TYPES = [DATA_PACK_TYPE, RESOURCE_PACK_TYPE, BEET_PROJECT_TYPE]


def path_prompt(
    path: str | None,
    prompt_mode: PromptMode = PromptMode.SHOW_PROMPTS,
) -> Path:
    """Validate the path or show a prompt if none is specified."""
    if not path and prompt_mode is PromptMode.SHOW_PROMPTS:
        path = text_prompt(
            title="Where do you want to create your project?",
            description="Press enter to use the current directory.",
        )

    return validate_path(path or __file__)


def type_prompt(
    project_type: BaseProjectType | None,
    prompt_mode: PromptMode = PromptMode.SHOW_PROMPTS,
) -> BaseProjectType:
    """Validate the project type or show a prompt if none is specified."""
    if not project_type and prompt_mode is PromptMode.SHOW_PROMPTS:
        project_type = single_option_prompt(
            title="What type of project do you want to create?",
            options=[
                Option(
                    value=project_type,
                    title=project_type.title,
                    description=project_type.description,
                )
                for project_type in PROJECT_TYPES
            ],
        )

    return project_type or BEET_PROJECT_TYPE


def description_prompt(
    description: str | None,
    prompt_mode: PromptMode = PromptMode.SHOW_PROMPTS,
) -> str:
    """Return the description or show a prompt if none is specified."""
    if not description and prompt_mode is PromptMode.SHOW_PROMPTS:
        description = text_prompt(
            title="What description do you want to add to your project?",
            description="Press enter to skip.",
        )

    return description or ""


def author_prompt(
    author: str | None,
    prompt_mode: PromptMode = PromptMode.SHOW_PROMPTS,
) -> str:
    """Return the author or show a prompt if none is specified."""
    git_username = get_git_username()

    if not author and prompt_mode is PromptMode.SHOW_PROMPTS:
        author = text_prompt(
            title="What author do you want to set to your project?",
            description="Press enter to use your Git username."
            if git_username
            else "Press enter to skip.",
        )

    return author or git_username or ""


def mc_version_prompt(
    mc_version: str | None,
    prompt_mode: PromptMode = PromptMode.SHOW_PROMPTS,
) -> MCVersion:
    """Validate the Minecraft version or show a prompt if none is specified."""
    fetch_mc_versions()

    if not mc_version and prompt_mode is PromptMode.SHOW_PROMPTS:
        mc_version = text_prompt(
            title="What Minecraft version do you want to use?",
            description="Press enter to use the latest release.",
        )

    return validate_mc_version(mc_version_str=mc_version or get_latest_release())


@rich_click.command()
@rich_click.argument(
    "path_str",
    required=False,
    help="The directory your project will be created at.",
)
@rich_click.option(
    "-y",
    "prompt_mode",
    flag_value=PromptMode.USE_DEFAULT,
    help="Use default values for all options.",
)
@rich_click.option(
    "--description",
    "description",
    help="What description you want to add to your project.",
)
@rich_click.option(
    "--author",
    "author",
    help="What author you want to set for your project.",
)
@rich_click.option(
    "--mc-version",
    "mc_version_str",
    help="What Minecraft version you want to use.",
)
@rich_click.option(
    "--type",
    "project_type",
    type=rich_click.Choice(
        choices=[project_type.option_id for project_type in PROJECT_TYPES],
        case_sensitive=False,
    ),
    help="What type of project you want to create.",
)
def create(
    path_str: str | None = None,
    prompt_mode: PromptMode = PromptMode.SHOW_PROMPTS,
    description: str | None = None,
    author: str | None = None,
    mc_version_str: str | None = None,
    project_type: BaseProjectType | None = None,
) -> None:
    """Scaffold a new project at PATH."""
    try:
        success_message(
            title="Welcome to PackSeed!",
            description="The Minecraft pack creator.",
            line_mode=LineMode.CLOSED_START,
        )

        prompt_mode = prompt_mode or PromptMode.SHOW_PROMPTS
        path = path_prompt(path=path_str, prompt_mode=prompt_mode)
        project_type = type_prompt(project_type=project_type, prompt_mode=prompt_mode)

        if project_type == DATA_PACK_TYPE:
            # ▄   ▗           ▌
            # ▌▌▀▌▜▘▀▌  ▛▌▀▌▛▘▙▘
            # ▙▘█▌▐▖█▌  ▙▌█▌▙▖▛▖
            #           ▌

            description = description_prompt(
                description=description,
                prompt_mode=prompt_mode,
            )
            mc_version = mc_version_prompt(
                mc_version=mc_version_str,
                prompt_mode=prompt_mode,
            )

            with Path.open(path / "pack.mcmeta", "x") as f:
                json.dump(
                    {
                        "pack": {
                            "description": description,
                            "min_format": [mc_version.data_pack_version],
                            "max_format": [mc_version.data_pack_version],
                        },
                    },
                    fp=f,
                    indent=2,
                )

            success_message("Data pack created.")

        if project_type == RESOURCE_PACK_TYPE:
            # ▄▖                      ▌
            # ▙▘█▌▛▘▛▌▌▌▛▘▛▘█▌  ▛▌▀▌▛▘▙▘
            # ▌▌▙▖▄▌▙▌▙▌▌ ▙▖▙▖  ▙▌█▌▙▖▛▖
            #                   ▌

            description = description_prompt(
                description=description,
                prompt_mode=prompt_mode,
            )
            mc_version = mc_version_prompt(
                mc_version=mc_version_str,
                prompt_mode=prompt_mode,
            )

            with Path.open(path / "pack.mcmeta", "x") as f:
                json.dump(
                    {
                        "pack": {
                            "description": description,
                            "min_format": [mc_version.resource_pack_version],
                            "max_format": [mc_version.resource_pack_version],
                        },
                    },
                    fp=f,
                    indent=2,
                )

            success_message("Resource pack created.")

        if project_type == BEET_PROJECT_TYPE:
            # ▄     ▗          ▘    ▗
            # ▙▘█▌█▌▜▘  ▛▌▛▘▛▌ ▌█▌▛▘▜▘
            # ▙▘▙▖▙▖▐▖  ▙▌▌ ▙▌ ▌▙▖▙▖▐▖
            #           ▌     ▙▌

            project_id = path.name
            description = description_prompt(
                description=description,
                prompt_mode=prompt_mode,
            )
            author = author_prompt(author=author, prompt_mode=prompt_mode)
            mc_version = mc_version_prompt(
                mc_version=mc_version_str,
                prompt_mode=prompt_mode,
            )

            with Path.open(path / "beet.json", "x") as f:
                json.dump(
                    {
                        "id": project_id,
                        "name": project_id,
                        "version": "0.1.0",
                        "description": description,
                        "author": author,
                        # FIXME @foxeddev: fix mc version for Beet
                        "minecraft": mc_version.id,
                        "output": "build",
                        "data_pack": {"load": ["src"]},
                        "resource_pack": {"load": ["src"]},
                    },
                    fp=f,
                    indent=2,
                )

            Path(path / "data" / project_id).mkdir(parents=True)
            Path(path / "assets" / project_id).mkdir(parents=True)

            success_message("Beet project created.")

    except KeyboardInterrupt:
        error_message("Bye!")
        sys.exit(1)

    except PackSeedError as err:
        error_message(err.title, err.description)
        sys.exit(1)
