import logging
import os

import click

from stactools.sentinel1.grd.stac import create_item

logger = logging.getLogger(__name__)


@click.group("grd")
def grd_cmd():
    """Commands for working with sentinel1 GRD data"""
    pass


@grd_cmd.command(
    "create-item",
    short_help="Convert a Sentinel1 GRD scene into a STAC item",
)
@click.argument("src")
@click.argument("dst")
def create_item_command(src, dst):
    """Creates a STAC Collection

    Args:
        src (str): path to the scene
        dst (str): path to the STAC Item JSON file that will be created
    """
    item = create_item(src)

    item_path = os.path.join(dst, "{}.json".format(item.id))
    item.set_self_href(item_path)

    item.save_object()
