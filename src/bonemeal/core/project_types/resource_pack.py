"""The registry for resource pack templates."""

from bonemeal.core.fields.template import Template

RESOURCE_PACK_TEMPLATES = {
    "minimal": Template(
        title="Minimal",
        description="only pack.mcmeta",
        includes=[
            "pack_mcmeta",
            "namespace",
        ],
    ),
    "default": Template(
        title="Default",
        description="pack.mcmeta, README, license",
        includes=[
            "pack_mcmeta",
            "readme",
            "license",
            "namespace",
        ],
    ),
}

DEFAULT_RESOURCE_PACK_TEMPLATE = 1
