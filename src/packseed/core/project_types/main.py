"""Register all project types."""

from packseed.cli.create.data_pack import create_data_pack
from packseed.cli.create.resource_pack import create_resource_pack
from packseed.core.project_types.project_type import ProjectType

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
