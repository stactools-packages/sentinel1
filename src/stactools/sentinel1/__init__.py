import stactools.core
from stactools.cli.registry import Registry

stactools.core.use_fsspec()


def register_plugin(registry: Registry) -> None:
    # Register subcommands
    from stactools.sentinel1 import commands

    registry.register_subcommand(commands.create_sentinel1_command)


__version__ = "0.8.0"
