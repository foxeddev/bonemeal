"""Command for creating a new resource pack."""

import rich_click

from bonemeal.cli.commons.messages import welcome_message
from bonemeal.cli.commons.prompts import (
    PromptLevel,
    description_prompt,
    mc_version_prompt,
    path_prompt,
)
from bonemeal.cli.utils.errors import handle_errors
from bonemeal.core.fields.mc_version import fetch_mc_versions
from bonemeal.core.generators.resource_pack import generate_resource_pack


def create_resource_pack(
    path_str: str | None = None,
    prompt_level: PromptLevel = PromptLevel.DEFAULT,
    description: str | None = None,
    mc_version_str: str | None = None,
) -> None:
    """Create a new resource pack at PATH."""
    prompt_level = prompt_level or PromptLevel.DEFAULT

    path = path_prompt(path_str, prompt_level)
    description = description_prompt(description, prompt_level)
    mc_version = mc_version_prompt(mc_version_str, prompt_level)

    generate_resource_pack(path=path, description=description, mc_version=mc_version)


@rich_click.command("resource-pack", aliases=["resource-pack", "resourcepack", "rp"])
@rich_click.argument("path_str", required=False)
@rich_click.option(
    "-y",
    "--yes",
    "prompt_level",
    flag_value=PromptLevel.NONE,
    help="Hide all interactive prompts and use default values instead.",
)
@rich_click.option("-d", "--description", help="The description of your resource pack.")
@rich_click.option(
    "-mc",
    "--mc-version",
    "mc_version_str",
    type=rich_click.Choice(fetch_mc_versions().values(), case_sensitive=False),
    help="The Minecraft version you want to create a resource pack for.",
    show_choices=False,
)
@handle_errors
def create_resource_pack_cmd(
    path_str: str | None = None,
    prompt_level: PromptLevel = PromptLevel.DEFAULT,
    description: str | None = None,
    mc_version_str: str | None = None,
) -> None:
    """Create a new resource pack at PATH."""
    welcome_message()

    create_resource_pack(
        path_str=path_str,
        prompt_level=prompt_level,
        description=description,
        mc_version_str=mc_version_str,
    )
