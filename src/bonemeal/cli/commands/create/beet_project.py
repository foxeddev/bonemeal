"""Command for creating a new Beet project."""

import rich_click

from bonemeal.cli.commons.messages import welcome_message
from bonemeal.cli.commons.prompts import (
    PromptLevel,
    author_prompt,
    config_type_prompt,
    description_prompt,
    mc_version_prompt,
    path_prompt,
    template_prompt,
)
from bonemeal.cli.components.message import info_message, success_message
from bonemeal.cli.utils.errors import handle_errors
from bonemeal.core.generators.beet_project import generate_beet_project
from bonemeal.core.project_types.beet_project import (
    BEET_CONFIG_TYPES,
    BEET_PROJECT_TEMPLATES,
    DEFAULT_BEET_CONFIG_TYPE,
    DEFAULT_BEET_PROJECT_TEMPLATE,
)


def create_beet_project(
    path_str: str | None = None,
    prompt_level: PromptLevel = PromptLevel.DEFAULT,
    author: str | None = None,
    description: str | None = None,
    mc_version_str: str | None = None,
    template_str: str | None = None,
    config_type_str: str | None = None,
) -> None:
    """Create a new Beet project."""
    prompt_level = prompt_level or PromptLevel.DEFAULT

    path = path_prompt(path_str, prompt_level)
    author = author_prompt(author, prompt_level)
    description = description_prompt(description, prompt_level)
    mc_version = mc_version_prompt(mc_version_str, prompt_level)
    template = template_prompt(
        template_str=template_str,
        templates=BEET_PROJECT_TEMPLATES,
        default_template=DEFAULT_BEET_PROJECT_TEMPLATE,
        prompt_level=prompt_level,
    )
    config_type = config_type_prompt(
        config_type_str=config_type_str,
        config_types=BEET_CONFIG_TYPES,
        default_config_type=DEFAULT_BEET_CONFIG_TYPE,
        prompt_level=prompt_level,
    )

    info_message("Creating Beet project...")

    generate_beet_project(
        path=path,
        author=author,
        description=description,
        mc_version=mc_version,
        template=template,
        config_type=config_type,
    )

    success_message("Beet project created!")


@rich_click.command("beet-project", aliases=["beet-project", "beet"])
@rich_click.argument(
    "path",
    required=False,
    help="Where you want to create your Beet project at.",
)
@rich_click.option(
    "-y",
    "--yes",
    "prompt_level",
    flag_value=PromptLevel.NONE,
    help="Hide all interactive prompts and use default values instead.",
)
@rich_click.option(
    "--author",
    help="The author of your Beet project.",
)
@rich_click.option(
    "--description",
    help="The description of your Beet project.",
)
@rich_click.option(
    "--mc-version",
    "mc_version_str",
    help="The Minecraft version you want to create a Beet project for.",
)
@rich_click.option(
    "--template",
    "template_str",
    help="The template you want to use for your Beet project.",
)
@rich_click.option(
    "--config-type",
    "config_type_str",
    help="The file type you want to use for Beet config files.",
)
@handle_errors
def create_beet_project_cmd(
    path: str,
    prompt_level: PromptLevel,
    author: str,
    description: str,
    mc_version_str: str,
    template_str: str,
    config_type_str: str,
) -> None:
    """Create a new Beet project."""
    welcome_message()

    create_beet_project(
        path_str=path,
        prompt_level=prompt_level,
        author=author,
        description=description,
        mc_version_str=mc_version_str,
        template_str=template_str,
        config_type_str=config_type_str,
    )
