import stactools.core
from stactools.cli.registry import Registry

from stactools.sentinel1.commands import create_sentinel1_command

stactools.core.use_fsspec()


def register_plugin(registry: Registry):
    # Register subcommands

    registry.register_subcommand(create_sentinel1_command)


__version__ = '0.2.0'
