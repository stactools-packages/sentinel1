import logging
import os

import click

from stactools.sentinel1.grd.stac import create_collection, create_item

from . import Format

logger = logging.getLogger(__name__)


@click.group("grd")
def grd_cmd() -> None:
    """Commands for working with sentinel1 GRD data"""
    pass


@grd_cmd.command(
    "create-collection", short_help="Create a Sentinel1 GRD STAC Collection"
)
@click.argument("destination")
def create_collection_command(destination: str) -> None:
    """Creates a STAC Collection for Sentinel1 GRD products"""

    collection = create_collection()
    json_path = os.path.join(destination, "sentinel1-grd.json")
    collection.set_self_href(os.path.join(os.path.basename(json_path)))
    collection.validate()
    collection.save_object(dest_href=json_path)


@grd_cmd.command(
    "create-item",
    short_help="Convert a Sentinel1 GRD scene into a STAC item",
)
@click.argument("src")
@click.argument("dst")
@click.option("--format", default="SAFE", type=str, help="SAFE or COG format")
def create_item_command(src: str, dst: str, format: str = "SAFE") -> None:
    """Creates a STAC Collection

    Args:
        src (str): path to the scene
        dst (str): path to the STAC Item JSON file that will be created
        format (str): Specifying the format of the granule. Currently supported formats
            are SAFE (default) and COG.
    """
    if format == "COG":
        archive_format = Format.COG
    else:
        archive_format = Format.SAFE

    item = create_item(src, archive_format=archive_format)

    item_path = os.path.join(dst, "{}.json".format(item.id))
    item.set_self_href(item_path)

    item.save_object()
