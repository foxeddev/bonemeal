from lib.cli.message import info_message

import rich_click


@rich_click.command()
@rich_click.argument("path", required=False)
def create(path):
    """Scaffold a new project at PATH.

    PATH is the directory your project will be created at.
    """

    info_message("Welcome to the Minecraft Pack Manager!", extend=0)
