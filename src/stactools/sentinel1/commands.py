import click

from stactools.sentinel1.grd.commands import grd_cmd
from stactools.sentinel1.rtc.commands import rtc_cmd
from stactools.sentinel1.slc.commands import slc_cmd


def create_sentinel1_command(cli: click.Group) -> click.Command:
    @cli.group("sentinel1")
    def sentinel1_cmd() -> None:
        """Commands for working with sentinel1 data"""
        pass

    sentinel1_cmd.add_command(grd_cmd)
    sentinel1_cmd.add_command(rtc_cmd)
    sentinel1_cmd.add_command(slc_cmd)

    return sentinel1_cmd
