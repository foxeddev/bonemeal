from pathlib import Path
from prompt_toolkit import HTML, print_formatted_text
from cli.prompt import prompt
from cli.choice import choice

import rich_click


@rich_click.command()
@rich_click.argument("path", required=False)
def create(path):
    """Scaffold a new Beep project at PATH.

    PATH is the directory your project will be created at.
    """

    print()
    print_formatted_text(HTML("<ansigreen>*</ansigreen> Welcome to the Beep CLI!"))
    print("│")

    if not path:
        path = prompt(
            message="Where do you want to create your project?",
            instructions=HTML("<gray>Press enter to use current directory.</gray>"),
        )
        print("│")

    path = (Path(path) if path else Path(__file__).parent).expanduser().resolve()

    if path.exists() and any(path.iterdir()):
        if not (
            choice(
                message="Directory not empty. Continue?",
                options=[(True, "Yes"), (False, "No")],
                default=1,
            )
        ):
            print()
            return
        print("│")
    else:
        path.mkdir(parents=True, exist_ok=True)

    print_formatted_text(HTML("<ansigreen>*</ansigreen> Project created!"))
    print("│")
    print_formatted_text(HTML("<ansigreen>*</ansigreen> You're all set!"))
    print()
