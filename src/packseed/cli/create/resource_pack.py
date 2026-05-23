"""Command for creating a new resource pack."""

import rich_click

from packseed.cli.errors import handle_errors
from packseed.cli.messages import welcome_message
from packseed.cli.prompts import (
    PromptMode,
    description_prompt,
    mc_version_prompt,
    path_prompt,
)
from packseed.core.generate.resource_pack import generate_resource_pack
from packseed.core.mc_version import fetch_mc_versions


@rich_click.command("resource-pack", aliases=["resourcepack", "rp"])
@rich_click.argument("path_str", required=False)
@rich_click.option(
    "-y",
    "--yes",
    "prompt_mode",
    flag_value=PromptMode.USE_DEFAULT,
    help="Hide all interactive prompts and use default values instead.",
)
@rich_click.option("-d", "--description", help="The description of your resource pack.")
@rich_click.option(
    "-mc",
    "--mc-version",
    "mc_version_str",
    type=rich_click.Choice(fetch_mc_versions(), case_sensitive=False),
    help="The Minecraft version you want to create a resource pack for.",
    show_choices=False,
)
@handle_errors
def create_resource_pack(
    path_str: str | None = None,
    prompt_mode: PromptMode = PromptMode.SHOW_PROMPTS,
    description: str | None = None,
    mc_version_str: str | None = None,
) -> None:
    """Create a new resource pack at PATH."""
    welcome_message()

    prompt_mode = prompt_mode or PromptMode.SHOW_PROMPTS
    path = path_prompt(path_str, prompt_mode)
    description = description_prompt(description, prompt_mode)
    mc_version = mc_version_prompt(mc_version_str, prompt_mode)

    generate_resource_pack(path=path, description=description, mc_version=mc_version)
