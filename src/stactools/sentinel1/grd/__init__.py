import stactools.core
from stactools.sentinel1_grd.stac import create_item

__all__ = ["create_item"]

stactools.core.use_fsspec()


def register_plugin(registry):
    from stactools.sentinel1_grd import commands

    registry.register_subcommand(commands.create_sentinel1grd_command)


__version__ = "0.1.0"
