"""Utilities."""

import rich_click

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


def add_command(group: rich_click.RichGroup, command: rich_click.RichCommand) -> None:
    """Add a command to a command group while inheriting all properties."""
    group.add_command(
        cmd=command,
        name=command.name,
        aliases=command.aliases,
        panel=command.panel,
    )
