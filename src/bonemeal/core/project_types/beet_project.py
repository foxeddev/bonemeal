"""The registry for data pack templates."""

import json

import tomlkit
import yaml

from bonemeal.core.fields.config_type import ConfigType

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

DEFAULT_BEET_CONFIG_TYPE = BEET_CONFIG_TYPES["json"]
