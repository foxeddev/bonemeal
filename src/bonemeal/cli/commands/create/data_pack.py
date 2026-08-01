"""Command for creating a new data pack."""

import rich_click

from bonemeal.cli.commons.messages import welcome_message
from bonemeal.cli.commons.prompts import (
    PromptLevel,
    author_prompt,
    description_prompt,
    mc_version_prompt,
    path_prompt,
    template_prompt,
)
from bonemeal.cli.components.message import info_message, success_message
from bonemeal.cli.utils.errors import handle_errors
from bonemeal.core.generators.data_pack import generate_data_pack
from bonemeal.core.project_types.data_pack import (
    DATA_PACK_TEMPLATES,
    DEFAULT_DATA_PACK_TEMPLATE,
)


def create_data_pack(
    path_str: str | None = None,
    prompt_level: PromptLevel = PromptLevel.DEFAULT,
    author: str | None = None,
    description: str | None = None,
    mc_version_str: str | None = None,
    template_str: str | None = None,
) -> None:
    """Create a new data pack."""
    prompt_level = prompt_level or PromptLevel.DEFAULT

    path = path_prompt(path_str, prompt_level)
    author = author_prompt(author, prompt_level)
    description = description_prompt(description, prompt_level)
    mc_version = mc_version_prompt(mc_version_str, prompt_level)
    template = template_prompt(
        template_str=template_str,
        templates=DATA_PACK_TEMPLATES,
        default_template=DEFAULT_DATA_PACK_TEMPLATE,
        prompt_level=prompt_level,
    )

    info_message("Creating data pack...")

    generate_data_pack(
        path=path,
        author=author,
        description=description,
        mc_version=mc_version,
        template=template,
    )

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
    "--author",
    help="The author of your data pack.",
)
@rich_click.option(
    "--description",
    help="The description of your data pack.",
)
@rich_click.option(
    "--mc-version",
    "mc_version_str",
    help="The Minecraft version you want to create a data pack for.",
)
@rich_click.option(
    "--template",
    "template_str",
    help="The template you want to use for your data pack.",
)
@handle_errors
def create_data_pack_cmd(
    path: str,
    prompt_level: PromptLevel,
    author: str,
    description: str,
    mc_version_str: str,
    template_str: str,
) -> None:
    """Create a new data pack."""
    welcome_message()

    create_data_pack(
        path_str=path,
        prompt_level=prompt_level,
        author=author,
        description=description,
        mc_version_str=mc_version_str,
        template_str=template_str,
    )
