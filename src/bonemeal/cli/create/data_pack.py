"""Command for creating a new data pack."""

import rich_click

from bonemeal.cli.errors import handle_errors
from bonemeal.cli.messages import welcome_message
from bonemeal.cli.prompts import (
    PromptMode,
    description_prompt,
    mc_version_prompt,
    path_prompt,
)
from bonemeal.core.generate.data_pack import generate_data_pack
from bonemeal.core.mc_version import fetch_mc_versions


@rich_click.command("data-pack", aliases=["datapack", "dp"])
@rich_click.argument("path_str", required=False)
@rich_click.option(
    "-y",
    "--yes",
    "prompt_mode",
    flag_value=PromptMode.USE_DEFAULT,
    help="Hide all interactive prompts and use default values instead.",
)
@rich_click.option("-d", "--description", help="The description of your data pack.")
@rich_click.option(
    "-mc",
    "--mc-version",
    "mc_version_str",
    type=rich_click.Choice(fetch_mc_versions(), case_sensitive=False),
    help="The Minecraft version you want to create a data pack for.",
    show_choices=False,
)
@handle_errors
def create_data_pack(
    path_str: str | None = None,
    prompt_mode: PromptMode = PromptMode.SHOW_PROMPTS,
    description: str | None = None,
    mc_version_str: str | None = None,
) -> None:
    """Create a new data pack at PATH."""
    welcome_message()

    prompt_mode = prompt_mode or PromptMode.SHOW_PROMPTS
    path = path_prompt(path_str, prompt_mode)
    description = description_prompt(description, prompt_mode)
    mc_version = mc_version_prompt(mc_version_str, prompt_mode)

    generate_data_pack(path=path, description=description, mc_version=mc_version)
