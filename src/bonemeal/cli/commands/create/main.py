"""Command for scaffolding a new project."""

from typing import TYPE_CHECKING

import rich_click

from bonemeal.cli.commons.messages import welcome_message
from bonemeal.cli.components.prompt import Choice, single_option_prompt
from bonemeal.cli.utils.commands import add_command
from bonemeal.cli.utils.errors import handle_errors
from bonemeal.core.project_types.main import PROJECT_TYPES

if TYPE_CHECKING:
    from bonemeal.core.project_types.project_type import ProjectType


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
    """Create a new project."""
    if not ctx.invoked_subcommand:
        welcome_message()

        project_type_prompt().create()


for project_type in PROJECT_TYPES.values():
    add_command(create_project, project_type.create_cmd)
