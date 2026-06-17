"""Main command group."""

import rich_click
from prompt_toolkit.shortcuts import set_title

from bonemeal.cli.commands import add_command
from bonemeal.cli.create.main import create_project
from bonemeal.cli.errors import handle_errors
from bonemeal.cli.list.main import list_project_types

help_config = rich_click.RichHelpConfiguration(
    style_option="blue",
    style_argument="blue",
    style_command="",
    style_switch="bold blue",
    style_metavar="",
    style_metavar_separator="",
    style_usage="bold blue",
    style_usage_command="",
    style_helptext_first_line="",
    style_helptext="dim ",
    style_option_default="dim ",
    style_required_short="bold red",
    style_required_long="red",
    style_options_panel_border="",
    style_commands_panel_border="",
)


@rich_click.group(context_settings={"help_option_names": ("-h", "--help")})
@rich_click.rich_config(help_config=help_config)
@handle_errors
def main() -> None:
    """The Minecraft pack management CLI."""  # noqa: D401
    set_title("🦴 Bone Meal, the Minecraft pack management CLI.")


add_command(main, create_project)
add_command(main, list_project_types)
