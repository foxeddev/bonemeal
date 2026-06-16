"""Command for creating a new Beet project."""

import rich_click

from bonemeal.cli.errors import handle_errors
from bonemeal.cli.messages import welcome_message
from bonemeal.cli.prompts import (
    PromptMode,
    author_prompt,
    description_prompt,
    mc_version_prompt,
    path_prompt,
)
from bonemeal.core.generate.beet_project import generate_beet_project
from bonemeal.core.mc_version import fetch_mc_versions


def create_beet_project(
    path_str: str | None = None,
    prompt_mode: PromptMode = PromptMode.SHOW_PROMPTS,
    author: str | None = None,
    description: str | None = None,
    mc_version_str: str | None = None,
) -> None:
    """Create a new Beet project at PATH."""
    prompt_mode = prompt_mode or PromptMode.SHOW_PROMPTS
    path = path_prompt(path_str, prompt_mode)
    author = author_prompt(author, prompt_mode)
    description = description_prompt(description, prompt_mode)
    mc_version = mc_version_prompt(mc_version_str, prompt_mode)

    generate_beet_project(
        path=path,
        author=author,
        description=description,
        mc_version=mc_version,
    )


@rich_click.command("beet-project", aliases=["beet-project", "beetproject", "beet"])
@rich_click.argument("path_str", required=False)
@rich_click.option(
    "-y",
    "--yes",
    "prompt_mode",
    flag_value=PromptMode.USE_DEFAULT,
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
    path_str: str | None = None,
    prompt_mode: PromptMode = PromptMode.SHOW_PROMPTS,
    author: str | None = None,
    description: str | None = None,
    mc_version_str: str | None = None,
) -> None:
    """Create a new Beet project at PATH."""
    welcome_message()

    create_beet_project(
        path_str=path_str,
        prompt_mode=prompt_mode,
        author=author,
        description=description,
        mc_version_str=mc_version_str,
    )
