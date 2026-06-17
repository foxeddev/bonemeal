"""The registry for all project types."""

from bonemeal.cli.commands.create.beet_project import (
    create_beet_project,
    create_beet_project_cmd,
)
from bonemeal.cli.commands.create.data_pack import (
    create_data_pack,
    create_data_pack_cmd,
)
from bonemeal.cli.commands.create.resource_pack import (
    create_resource_pack,
    create_resource_pack_cmd,
)
from bonemeal.core.project_types.project_type import ProjectType

PROJECT_TYPES: dict[str, ProjectType] = {
    "data_pack": ProjectType(
        create=create_data_pack,
        create_cmd=create_data_pack_cmd,
        title="Data pack",
    ),
    "resource_pack": ProjectType(
        create=create_resource_pack,
        create_cmd=create_resource_pack_cmd,
        title="Resource pack",
    ),
    "beet_project": ProjectType(
        create=create_beet_project,
        create_cmd=create_beet_project_cmd,
        title="Beet project",
    ),
}
