"""Function for generating a new data pack."""

import json
import os
from pathlib import Path
from typing import TYPE_CHECKING

from bonemeal.core.utils.generators import (
    generate_mit_license,
    generate_readme,
    id_to_name,
)

if TYPE_CHECKING:
    from bonemeal.core.fields.mc_version import MCVersion
    from bonemeal.core.fields.template import Template


def generate_data_pack(
    path: Path,
    author: str,
    description: str,
    mc_version: MCVersion,
    template: Template,
) -> None:
    """Generate a new data pack."""
    path = path.expanduser().resolve()
    os.chdir(path)

    project_id = path.name
    project_name = id_to_name(project_id)

    if "pack_mcmeta" in template.includes:
        with Path.open(path / "pack.mcmeta", "x") as f:
            json.dump(
                {
                    "pack": {
                        "description": description,
                        "min_format": mc_version.data_pack_version,
                        "max_format": mc_version.data_pack_version,
                    },
                },
                fp=f,
                indent=2,
            )

    if "readme" in template.includes:
        with Path.open(path / "README.md", "x") as f:
            f.write(generate_readme(project_name, description))

    if "license" in template.includes:
        with Path.open(path / "LICENSE", "x") as f:
            f.write(generate_mit_license(author))

    if "namespace" in template.includes:
        Path.mkdir(path / "data" / project_id, parents=True)

        if "load_tick" in template.includes:
            load_tag_path = (
                path / "data" / "minecraft" / "tags" / "function" / "load.json"
            )
            Path.mkdir(load_tag_path.parent, parents=True)
            with Path.open(load_tag_path, "x") as f:
                json.dump(
                    {
                        "values": [
                            f"{project_id}:load",
                        ],
                    },
                    f,
                    indent=2,
                )

            tick_tag_path = (
                path / "data" / "minecraft" / "tags" / "function" / "tick.json"
            )
            Path.mkdir(tick_tag_path.parent, parents=True)
            with Path.open(tick_tag_path, "x") as f:
                json.dump(
                    {
                        "values": [
                            f"{project_id}:tick",
                        ],
                    },
                    f,
                    indent=2,
                )

            load_function_path = (
                path / "data" / project_id / "function" / "load.mcfunction"
            )
            Path.mkdir(load_function_path.parent, parents=True)
            Path.touch(load_function_path)

            tick_function_path = (
                path / "data" / project_id / "function" / "tick.mcfunction"
            )
            Path.mkdir(tick_function_path.parent, parents=True)
            Path.touch(tick_function_path)
