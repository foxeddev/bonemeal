import rich_click
from prompt_toolkit.shortcuts import set_title

from create import create


@rich_click.group()
def main() -> None:
    set_title("PackSeed - The Minecraft pack creator.")


main.add_command(create)


if __name__ == "__main__":
    main()
