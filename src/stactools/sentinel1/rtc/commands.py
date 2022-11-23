import json
import logging
import os

import click

from stactools.sentinel1.rtc.stac import create_collection, create_item

logger = logging.getLogger(__name__)


@click.group("rtc")
def rtc_cmd() -> None:
    """Commands for working with sentinel1 RTC data"""
    pass


@rtc_cmd.command(
    "create-collection", short_help="Create a Sentinel1 RTC STAC Collection"
)
@click.argument("destination")
def create_collection_command(destination: str) -> None:
    """Creates a STAC Collection for Sentinel1 RTC products"""

    collection = create_collection()
    json_path = os.path.join(destination, "sentinel1-rtc.json")
    collection.set_self_href(os.path.join(os.path.basename(json_path)))
    collection.validate()
    collection.save_object(dest_href=json_path)


@rtc_cmd.command(
    "create-item", short_help="Convert a Sentinel1 RTC product into a STAC item"
)
@click.argument("src")
@click.argument("dst")
@click.option(
    "-a",
    "--asset",
    default="local_incident_angle.tif",
    help="Asset geotiff metadata to read",
)
@click.option(
    "-p",
    "--providers",
    help="Path to JSON file containing array of additional providers",
)
@click.option(
    "-m",
    "--metadata",
    is_flag=True,
    default=False,
    help="Include links to original GRD metadata as STAC Assets",
)
def create_item_command(
    src: str, dst: str, asset: str, providers: str, metadata: bool
) -> None:
    """Creates a STAC Item for a given Sentinel1 RTC product

    SRC is the path to the granule
    DST is directory that a STAC Item JSON file will be created
    in. for example, ./S1B_20161121_12SYJ_ASC/S1B_20161121_12SYJ_ASC.json
    """
    additional_providers = None
    if providers is not None:
        with open(providers) as f:
            additional_providers = json.load(f)

    item = create_item(
        src,
        asset,
        additional_providers=additional_providers,
        include_grd_metadata=metadata,
    )
    item_path = os.path.join(dst, f"{item.id}.json")
    item.set_self_href(item_path)
    item.save_object()
