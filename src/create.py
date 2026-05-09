from enum import Enum, auto

from lib.cli.message import error_message, success_message

from lib.cli.prompt import Option, option_prompt, text_prompt
import rich_click


class Template(Enum):
    dp = auto()
    rp = auto()
    beet = auto()


@rich_click.command()
@rich_click.argument("path", required=False)
@rich_click.option(
    "--template",
    type=rich_click.Choice(Template),
    help="What type of project you want to create.",
)
def create(path: str, template: int) -> None:
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
            template = option_prompt(
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

        success_message("You're all set!")

    except KeyboardInterrupt:
        error_message("Bye!")
