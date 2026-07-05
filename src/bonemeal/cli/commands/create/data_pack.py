"""Command for creating a new data pack."""

import rich_click

from bonemeal.cli.commons.messages import welcome_message
from bonemeal.cli.commons.prompts import (
    PromptLevel,
    description_prompt,
    mc_version_prompt,
    path_prompt,
)
from bonemeal.cli.components.message import info_message, success_message
from bonemeal.cli.utils.errors import handle_errors
from bonemeal.core.generators.data_pack import generate_data_pack


def create_data_pack(
    path_str: str | None = None,
    prompt_level: PromptLevel = PromptLevel.DEFAULT,
    description: str | None = None,
    mc_version_str: str | None = None,
) -> None:
    """Create a new data pack."""
    prompt_level = prompt_level or PromptLevel.DEFAULT

    path = path_prompt(path_str, prompt_level)
    description = description_prompt(description, prompt_level)
    mc_version = mc_version_prompt(mc_version_str, prompt_level)

    info_message("Creating data pack...")

    generate_data_pack(path=path, description=description, mc_version=mc_version)

    success_message("Data pack created!")


@rich_click.command("data-pack", aliases=["data-pack", "datapack", "dp"])
@rich_click.argument(
    "path",
    required=False,
    help="Where you want to create your data pack at.",
)
@rich_click.option(
    "-y",
    "--yes",
    "prompt_level",
    flag_value=PromptLevel.NONE,
    help="Hide all interactive prompts and use default values instead.",
)
@rich_click.option(
    "-d",
    "--description",
    help="The description of your data pack.",
)
@rich_click.option(
    "-m",
    "--mc-version",
    "mc_version_str",
    help="The Minecraft version you want to create a data pack for.",
)
@handle_errors
def create_data_pack_cmd(
    path: str,
    prompt_level: PromptLevel,
    description: str,
    mc_version_str: str,
) -> None:
    """Create a new data pack."""
    welcome_message()

    create_data_pack(
        path_str=path,
        prompt_level=prompt_level,
        description=description,
        mc_version_str=mc_version_str,
    )
