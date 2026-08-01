"""Function for generating a new resource pack."""

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


def generate_resource_pack(
    path: Path,
    author: str,
    description: str,
    mc_version: MCVersion,
) -> None:
    """Generate a new resource pack."""
    path = path.expanduser().resolve()
    os.chdir(path)

    project_id = path.name
    project_name = id_to_name(project_id)

    with Path.open(path / "pack.mcmeta", "x") as f:
        json.dump(
            {
                "pack": {
                    "description": description,
                    "min_format": mc_version.resource_pack_version,
                    "max_format": mc_version.resource_pack_version,
                },
            },
            fp=f,
            indent=2,
        )

    with Path.open(path / "README.md", "x") as f:
        f.write(generate_readme(project_name, description))

    with Path.open(path / "LICENSE", "x") as f:
        f.write(generate_mit_license(author))

    Path.mkdir(path / "assets" / project_id, parents=True)
