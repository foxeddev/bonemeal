"""The registry for data pack templates."""

from bonemeal.core.fields.template import Template

DATA_PACK_TEMPLATES = {
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
        description="pack.mcmeta, README, license, tick and load functions",
        includes=[
            "pack_mcmeta",
            "readme",
            "license",
            "namespace",
            "load_tick",
        ],
    ),
}

DEFAULT_DATA_PACK_TEMPLATE = 1
