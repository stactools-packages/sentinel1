import click

from stactools.sentinel1.grd import commands as grd_commands
from stactools.sentinel1.rtc import commands as rtc_commands


def create_sentinel1_command(cli: click.Group) -> click.Command:
    @cli.group('sentinel1')
    def sentinel1_cmd():
        """Commands for working with sentinel1 data"""
        pass

    sentinel1_cmd.add_command(grd_commands.grd_cmd)
    sentinel1_cmd.add_command(rtc_commands.rtc_cmd)

    return sentinel1_cmd
