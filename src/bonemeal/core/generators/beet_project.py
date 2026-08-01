"""Function for generating a new data pack."""

import os
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

import tomlkit

from bonemeal.core.errors.main import BoneMealError
from bonemeal.core.utils.commands import run
from bonemeal.core.utils.generators import (
    generate_mit_license,
    generate_readme,
    id_to_name,
)

if TYPE_CHECKING:
    from bonemeal.core.fields.config_type import ConfigType
    from bonemeal.core.fields.mc_version import MCVersion


class UVNotFoundError(BoneMealError):
    """Error raised when the `uv`-command raises an error."""

    title = "Could not find uv installation!"
    description = "Make sure to install uv: https://docs.astral.sh/uv/"


class UVExecutionError(BoneMealError):
    """Error raised when the `uv`-command raises an error."""

    title = "uv raised an error!"


def generate_beet_project(
    path: Path,
    author: str,
    description: str,
    mc_version: MCVersion,
    config_type: ConfigType,
) -> None:
    """Generate a new data pack."""
    path = path.expanduser().resolve()
    os.chdir(path)

    project_id = path.name
    project_name = id_to_name(project_id)

    # Generate Beet config

    config = {
        "id": project_id,
        "name": project_name,
        "version": "0.1.0",
        "author": author,
        "description": description,
        "minecraft": mc_version.id,
        "output": "build",
        "data_pack": {
            "load": [
                "src",
            ],
        },
        "resource_pack": {
            "load": [
                "src",
            ],
        },
    }

    # Write Beet config

    with Path.open(path / config_type.file, "x") as f:
        config_type.write(config, f)

    # Generate pyproject.toml

    pyproject_toml = {
        "name": project_id,
        "version": "0.1.0",
        "dependencies": [
            "beet>=0.115.0",
            "bolt>=0.50.1",
            "bolt-expressions>=0.19.2",
            "mecha>=0.103.0",
            "ruff>=0.15.17",
        ],
        "requires-python": ">=3.14",
        "authors": [{"name": author}],
        "description": description,
        "readme": "README.md",
        "license": "MIT",
        "license-files": ["LICENSE"],
    }

    # Write pyproject.toml

    with Path.open(path / "pyproject.toml", "x") as f:
        tomlkit.dump(
            pyproject_toml,
            fp=f,
        )

    # Write README.md

    with Path.open(path / "README.md", "x") as f:
        f.write(generate_readme(project_name, description))

    with Path.open(path / "LICENSE", "x") as f:
        f.write(generate_mit_license(author))

    # Make namespaced directories

    Path.mkdir(path / "src" / "data" / path.name, parents=True)
    Path.mkdir(path / "src" / "assets" / path.name, parents=True)

    # Set up uv

    try:
        run(["uv", "sync"])
    except FileNotFoundError as err:
        raise UVNotFoundError from err
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as err:
        raise UVExecutionError from err
