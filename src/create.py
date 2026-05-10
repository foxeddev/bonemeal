from enum import Enum, auto

from lib.cli.message import error_message, success_message

from lib.cli.prompt import (
    Option,
    multi_option_prompt,
    single_option_prompt,
    text_prompt,
)
import rich_click


class Template(Enum):
    dp = auto()
    rp = auto()
    beet = auto()


class Addon(Enum):
    smithed = auto()
    stewbeet = auto()


@rich_click.command()
@rich_click.argument("path", required=False)
@rich_click.option(
    "--template",
    type=rich_click.Choice(Template),
    multiple=True,
    help="What type of project you want to create.",
)
@rich_click.option(
    "--addons",
    type=rich_click.Choice(Addon),
    help="What add-ons you want to add to your project.",
)
def create(path: str, template: int, addons: list[int]) -> None:
    """Scaffold a new project at PATH.

    PATH is the directory your project will be created at.
    """

    success_message(
        title="Welcome to PackSeed!",
        description="The Minecraft pack creator.",
        connect=False,
    )

    try:
        if not path:
            path = text_prompt(
                title="Where do you want to create your project?",
                description="Press enter to use the current directory.",
            )

        if not template:
            template = single_option_prompt(
                title="What template do you want to use?",
                options=[
                    Option("Vanilla data pack"),
                    Option("Vanilla resource pack"),
                    Option(
                        "Beet project",
                        "Beet is a Minecraft pack development kit for both data packs and resource packs.",
                    ),
                ],
            )

        success_message("Project created.")

        if not addons:
            template = multi_option_prompt(
                title="What add-ons do you want to add?",
                description="Use space to select/deselect options.",
                options=[
                    Option("Smithed conventions"),
                    Option("StewBeet"),
                ],
            )

        success_message("You're all set!")

    except KeyboardInterrupt:
        error_message("Bye!")
