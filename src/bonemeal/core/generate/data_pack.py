"""Function to generate a new data pack."""

import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bonemeal.core.mc_version import MCVersion


def generate_data_pack(
    path: Path,
    description: str | None,
    mc_version: MCVersion,
) -> None:
    """Generate a new data pack."""
    with Path.open(path / "pack.mcmeta", "x") as f:
        json.dump(
            {
                "pack": {
                    "description": description,
                    "min_format": [mc_version.data_pack_version],
                    "max_format": [mc_version.data_pack_version],
                },
            },
            fp=f,
            indent=2,
        )

    Path.mkdir(path / "data" / path.name, parents=True)
