"""Function to generate a new data pack."""

import os
import subprocess
from pathlib import Path

from tomlkit import TOMLDocument, array, document, dump, inline_table, table

from bonemeal.cli.errors import BoneMealError
from bonemeal.core.utils import run_silent


def generate_pyproject_toml(
    project_id: str,
    project_name: str,
    author: str,
    description: str,
) -> TOMLDocument:
    """Generate a `pyproject.toml`-file for a Beet project."""
    doc = document()

    project = table()
    project["name"] = project_id
    project["version"] = "0.1.0"
    project["dependencies"] = [
        "beet>=0.115.0",
        "bolt>=0.50.1",
        "bolt-expressions>=0.19.2",
        "mecha>=0.103.0",
        "ruff>=0.15.17",
    ]
    project["requires-python"] = ">=3.14"
    project["authors"] = array()
    project["authors"].append(inline_table().add("name", author))
    project["description"] = ""
    project["readme"] = "README.md"
    project["license"] = "MIT"
    project["license-files"] = ["LICENSE"]

    doc["project"] = project

    tool = table()
    beet = table()

    beet["id"] = project_id
    beet["name"] = project_name
    beet["version"] = "0.1.0"
    beet["author"] = author
    beet["description"] = description
    beet["minecraft"] = "26.1"
    beet["output"] = "build"
    beet["data_pack"] = inline_table().add("load", "src")
    beet["resource_pack"] = inline_table().add("load", "src")

    tool["beet"] = beet
    doc["tool"] = tool

    return doc


class UVError(BoneMealError):
    """Error raised when the `uv`-command raises an error."""

    title = "Could not find uv installation!"
    description = "Make sure to install uv: https://docs.astral.sh/uv/"


def generate_beet_project(
    path: Path,
    author: str,
    description: str,
) -> None:
    """Generate a new data pack."""
    path = path.expanduser().resolve()
    project_id = path.name
    project_name = project_id.replace("-", " ").replace("_", " ").strip().capitalize()

    os.chdir(path)

    with Path.open(path / "pyproject.toml", "x") as f:
        dump(
            generate_pyproject_toml(
                project_id=project_id,
                project_name=project_name,
                author=author,
                description=description,
            ),
            fp=f,
        )

    with Path.open(path / "README.md", "x") as f:
        f.write(f"# {project_name}{f'\n\n{description}' if description else ''}\n")

    Path.mkdir(path / "src" / "data" / path.name, parents=True)
    Path.mkdir(path / "src" / "assets" / path.name, parents=True)

    try:
        run_silent(["uv", "venv", ".venv"])
        run_silent(["uv", "sync"])
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as err:
        raise UVError from err
