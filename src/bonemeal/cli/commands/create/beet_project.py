"""Command for creating a new Beet project."""

import rich_click

from bonemeal.cli.commons.messages import welcome_message
from bonemeal.cli.commons.prompts import (
    PromptLevel,
    author_prompt,
    description_prompt,
    mc_version_prompt,
    path_prompt,
)
from bonemeal.cli.components.message import info_message, success_message
from bonemeal.cli.utils.errors import handle_errors
from bonemeal.core.fields.mc_version import fetch_mc_versions
from bonemeal.core.generators.beet_project import generate_beet_project


def create_beet_project(
    path_str: str | None = None,
    prompt_level: PromptLevel = PromptLevel.DEFAULT,
    author: str | None = None,
    description: str | None = None,
    mc_version_str: str | None = None,
) -> None:
    """Create a new Beet project."""
    prompt_level = prompt_level or PromptLevel.DEFAULT

    path = path_prompt(path_str, prompt_level)
    author = author_prompt(author, prompt_level)
    description = description_prompt(description, prompt_level)
    mc_version = mc_version_prompt(mc_version_str, prompt_level)

    info_message("Creating Beet project...")

    generate_beet_project(
        path=path,
        author=author,
        description=description,
        mc_version=mc_version,
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
@rich_click.option("-a", "--author", help="The author of your Beet project.")
@rich_click.option("-d", "--description", help="The description of your Beet project.")
@rich_click.option(
    "-mc",
    "--mc-version",
    "mc_version_str",
    type=rich_click.Choice(fetch_mc_versions().values(), case_sensitive=False),
    help="The Minecraft version you want to create a data pack for.",
    show_choices=False,
)
@handle_errors
def create_beet_project_cmd(
    path: str,
    prompt_level: PromptLevel,
    author: str,
    description: str,
    mc_version_str: str,
) -> None:
    """Create a new Beet project."""
    welcome_message()

    create_beet_project(
        path_str=path,
        prompt_level=prompt_level,
        author=author,
        description=description,
        mc_version_str=mc_version_str,
    )
