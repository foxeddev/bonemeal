"""Function for generating a new data pack."""

import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bonemeal.core.fields.mc_version import MCVersion
    from bonemeal.core.fields.template import Template


def generate_data_pack(
    path: Path,
    description: str,
    mc_version: MCVersion,
    template: Template,
) -> None:
    """Generate a new data pack."""
    namespace = path.name

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

    if "namespace" in template.includes:
        Path.mkdir(path / "data" / namespace, parents=True, exist_ok=True)

        if "load_tick" in template.includes:
            load_tag_path = (
                path / "data" / "minecraft" / "tags" / "function" / "load.json"
            )
            Path.mkdir(load_tag_path.parent, parents=True, exist_ok=True)
            with Path.open(load_tag_path, "x") as f:
                json.dump(
                    {
                        "values": [
                            f"{namespace}:load",
                        ],
                    },
                    f,
                    indent=2,
                )

            tick_tag_path = (
                path / "data" / "minecraft" / "tags" / "function" / "tick.json"
            )
            Path.mkdir(tick_tag_path.parent, parents=True, exist_ok=True)
            with Path.open(tick_tag_path, "x") as f:
                json.dump(
                    {
                        "values": [
                            f"{namespace}:tick",
                        ],
                    },
                    f,
                    indent=2,
                )

            load_function_path = (
                path / "data" / namespace / "function" / "load.mcfunction"
            )
            Path.mkdir(load_function_path.parent, parents=True, exist_ok=True)
            Path.touch(load_function_path)

            tick_function_path = (
                path / "data" / namespace / "function" / "tick.mcfunction"
            )
            Path.mkdir(tick_function_path.parent, parents=True, exist_ok=True)
            Path.touch(tick_function_path)
