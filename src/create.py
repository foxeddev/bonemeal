from enum import Enum, auto
import json
from pathlib import Path

from prompt_toolkit import HTML
from send2trash import send2trash

from lib.cli.message import error_message, success_message

from lib.cli.prompt import (
    Option,
    single_option_prompt,
    text_prompt,
)
import rich_click


class Template(Enum):
    DATA_PACK = auto()
    RESOURCE_PACK = auto()


@rich_click.command()
@rich_click.argument("path", required=False)
@rich_click.option(
    "--template",
    type=rich_click.Choice(choices=Template, case_sensitive=False),
    help="What type of project you want to create.",
)
def create(path: str, template: Template) -> None:
    """Scaffold a new project at PATH.

    PATH is the directory your project will be created at.
    """

    success_message(
        title="Welcome to PackSeed!",
        description="The Minecraft pack creator.",
        connect=False,
    )

    path = path.strip() if path else ""

    try:
        if not path:
            path = text_prompt(
                title="Where do you want to create your project?",
                description="Press enter to use the current directory.",
            )

        path = path.strip() if path else ""

        full_path = Path(path).resolve()

        if full_path.is_dir(follow_symlinks=False):
            if any(full_path.iterdir()):
                if not single_option_prompt(
                    title="The specified directory is not empty. Do you want to overwrite it?",
                    options=[
                        Option(value=True, title="OK"),
                        Option(value=False, title="Cancel"),
                    ],
                    default_option=1,
                    icon=HTML("<ansiyellow>!</ansiyellow>"),
                ):
                    exit(0)
                else:
                    send2trash(full_path)

        elif full_path.exists():
            if not single_option_prompt(
                title="A file with the specified name already exists. Do you want to overwrite it?",
                options=[
                    Option(value=True, title="OK"),
                    Option(value=False, title="Cancel"),
                ],
                default_option=1,
                icon=HTML("<ansiyellow>!</ansiyellow>"),
            ):
                exit(0)
            else:
                send2trash(full_path)

        if not template:
            template = single_option_prompt(
                title="What template do you want to use?",
                options=[
                    Option(value=Template.DATA_PACK, title="Data Pack"),
                    Option(value=Template.RESOURCE_PACK, title="Resource Pack"),
                ],
            )

    except KeyboardInterrupt:
        error_message("Bye!")
        exit(1)

    full_path.mkdir(exist_ok=True, parents=True)

    if template == Template.DATA_PACK:
        with open(full_path / "pack.mcmeta", "x") as f:
            json.dump(
                {
                    "pack": {
                        "description": "",
                        "min_format": [
                            101,
                            1,
                        ],
                        "max_format": [
                            101,
                            1,
                        ],
                    }
                },
                f,
                indent=2,
            )

    success_message("Project created.")

    success_message("You're all set!")
