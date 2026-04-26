from create import create

import rich_click


@rich_click.group()
def main():
    pass


main.add_command(create)


if __name__ == "__main__":
    main()
