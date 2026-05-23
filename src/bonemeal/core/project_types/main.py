"""Register all project types."""

from bonemeal.cli.create.data_pack import create_data_pack
from bonemeal.cli.create.resource_pack import create_resource_pack
from bonemeal.core.project_types.project_type import ProjectType

PROJECT_TYPES: dict[str, ProjectType] = {
    "data_pack": ProjectType(
        create=create_data_pack,
        title="Data pack",
    ),
    "resource_pack": ProjectType(
        create=create_resource_pack,
        title="Resource pack",
    ),
}
