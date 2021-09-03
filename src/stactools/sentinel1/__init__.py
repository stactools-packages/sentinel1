import stactools.core

from stactools.sentinel1.commands import create_sentinel1_command
from stactools.cli.registry import Registry

stactools.core.use_fsspec()


def register_plugin(registry: Registry):
    # Register subcommands

    registry.register_subcommand(create_sentinel1_command)


__version__ = '0.1.0'
