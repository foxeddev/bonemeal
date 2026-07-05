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
        description="pack.mcmeta, tick and load functions",
        includes=[
            "pack_mcmeta",
            "namespace",
            "load_tick",
        ],
    ),
}
