"""Main command group."""

import rich_click
from prompt_toolkit.shortcuts import set_title

from packseed.cli.create.main import create_project
from packseed.cli.errors import handle_errors
from packseed.cli.list.main import list_project_types
from packseed.cli.utils import add_command


@rich_click.group(context_settings={"help_option_names": ("-h", "--help")})
@handle_errors
def main() -> None:
    """Create and manage Minecraft packs."""
    set_title("PackSeed - The Minecraft pack manager.")


add_command(main, create_project)
add_command(main, list_project_types)
