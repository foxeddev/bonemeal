"""The registry for data pack templates."""

import json

import tomlkit
import yaml

from bonemeal.core.fields.config_type import ConfigType
from bonemeal.core.fields.template import Template

BEET_PROJECT_TEMPLATES = {
    "minimal": Template(
        title="Minimal",
        description="only Beet config",
        includes=[
            "beet_config",
            "namespace",
        ],
    ),
    "default": Template(
        title="Default",
        description="Beet config, pyproject.toml, README, license, uv setup",
        includes=[
            "beet_config",
            "pyproject_toml",
            "readme",
            "license",
            "namespace",
            "uv",
        ],
    ),
}

DEFAULT_BEET_PROJECT_TEMPLATE = 1


BEET_CONFIG_TYPES = {
    "json": ConfigType(
        title="JSON",
        file="beet.json",
        write=lambda content, file: json.dump(content, file, indent=2),
    ),
    "yaml": ConfigType(
        title="YAML",
        file="beet.yaml",
        write=lambda content, file: yaml.dump(content, file, indent=2, sort_keys=False),
    ),
    "toml": ConfigType(
        title="TOML",
        file="beet.toml",
        write=tomlkit.dump,
    ),
}

DEFAULT_BEET_CONFIG_TYPE = 0
