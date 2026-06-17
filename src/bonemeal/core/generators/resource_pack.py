"""Function for generating a new resource pack."""

import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bonemeal.core.mc_version import MCVersion


def generate_resource_pack(
    path: Path,
    description: str,
    mc_version: MCVersion,
) -> None:
    """Generate a new resource pack."""
    with Path.open(path / "pack.mcmeta", "x") as f:
        json.dump(
            {
                "pack": {
                    "description": description,
                    "min_format": [mc_version.resource_pack_version],
                    "max_format": [mc_version.resource_pack_version],
                },
            },
            fp=f,
            indent=2,
        )

    Path.mkdir(path / "assets" / path.name, parents=True)
