"""Main command group."""

import rich_click
from prompt_toolkit.shortcuts import set_title

from bonemeal.cli.create.main import create_project
from bonemeal.cli.errors import handle_errors
from bonemeal.cli.list.main import list_project_types
from bonemeal.cli.utils import add_command, help_config


@rich_click.group(context_settings={"help_option_names": ("-h", "--help")})
@rich_click.rich_config(help_config=help_config)
@handle_errors
def main() -> None:
    """The Minecraft pack management CLI."""  # noqa: D401
    set_title("🦴 Bone Meal, the Minecraft pack management CLI.")


add_command(main, create_project)
add_command(main, list_project_types)
