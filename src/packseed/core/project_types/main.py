"""Register all project types."""

from packseed.cli.create.data_pack import create_data_pack
from packseed.cli.create.resource_pack import create_resource_pack
from packseed.core.project_types.project_type import ProjectType

PROJECT_TYPES: dict[str, ProjectType] = {
    "data_pack": ProjectType(
        id="data_pack",
        name="data-pack",
        create=create_data_pack,
        aliases=["datapack", "dp"],
        title="Data pack",
    ),
    "resource_pack": ProjectType(
        id="resource_pack",
        name="resource-pack",
        create=create_resource_pack,
        aliases=["resourcepack", "rp"],
        title="Resource pack",
    ),
}
