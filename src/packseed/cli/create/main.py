"""Command for scaffolding a new project."""

from typing import TYPE_CHECKING

import rich_click

from packseed.cli.components.prompt import Choice, single_option_prompt
from packseed.cli.errors import handle_errors
from packseed.cli.messages import welcome_message
from packseed.cli.utils import add_command
from packseed.core.project_types.main import PROJECT_TYPES

if TYPE_CHECKING:
    from packseed.core.project_types.project_type import ProjectType


def project_type_prompt() -> ProjectType:
    """Validate the project type or show a prompt if none is specified."""
    return single_option_prompt(
        title="What type of project do you want to create?",
        options=[
            Choice(
                value=project_type,
                title=project_type.title,
                description=project_type.description,
            )
            for project_type in PROJECT_TYPES.values()
        ],
    )


@rich_click.group("create", invoke_without_command=True)
@rich_click.pass_context
@handle_errors
def create_project(ctx: rich_click.Context) -> None:
    """Scaffold a new project at PATH."""
    if not ctx.invoked_subcommand:
        welcome_message()

        project_type = project_type_prompt()

        if project_type.create.callback:
            project_type.create.callback()


for project_type in PROJECT_TYPES.values():
    add_command(create_project, project_type.create)
