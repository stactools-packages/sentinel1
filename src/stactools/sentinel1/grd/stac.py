import logging
import os
from typing import Any, Optional

import pystac
import shapely
from pystac import Summaries
from pystac.extensions.eo import EOExtension
from pystac.extensions.item_assets import ItemAssetsExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.sar import SarExtension
from pystac.extensions.sat import SatExtension
from stactools.core.io import ReadHrefModifier
from stactools.core.projection import transform_from_bbox

from ..bands import image_asset_from_href
from ..formats import Format
from ..metadata_links import MetadataLinks
from ..product_metadata import get_shape
from . import constants as c
from .product_metadata import GRDProductMetadata
from .properties import fill_sar_properties, fill_sat_properties

logger = logging.getLogger(__name__)


def create_collection(json_path: str) -> pystac.Collection:
    """Creates a STAC Collection for Sentinel-1 RTC"""
    # Lists of all possible values for items
    summary_dict = {
        "constellation": [c.SENTINEL_CONSTELLATION],
        "platform": c.SENTINEL_PLATFORMS,
    }

    collection = pystac.Collection(
        id="sentinel1-grd",
        description=c.SENTINEL_GRD_DESCRIPTION,
        extent=c.SENTINEL_GRD_EXTENT,
        title="Sentinel-1 GRD",
        href=json_path,
        stac_extensions=[
            SarExtension.get_schema_uri(),
            SatExtension.get_schema_uri(),
            EOExtension.get_schema_uri(),
        ],
        keywords=c.SENTINEL_GRD_KEYWORDS,
        providers=[c.SENTINEL_PROVIDER, c.SENTINEL_GRD_PROVIDER],
        summaries=Summaries(summary_dict),
    )

    # Links
    collection.links.append(c.SENTINEL_GRD_LICENSE)
    collection.links.append(c.SENTINEL_GRD_TECHNICAL_GUIDE)

    # SAR Extension
    sar = SarExtension.summaries(collection, add_if_missing=True)
    sar.looks_range = c.SENTINEL_GRD_SAR["looks_range"]
    sar.product_type = c.SENTINEL_GRD_SAR["product_type"]
    sar.looks_azimuth = c.SENTINEL_GRD_SAR["looks_azimuth"]
    sar.polarizations = c.SENTINEL_GRD_SAR["polarizations"]
    sar.frequency_band = c.SENTINEL_GRD_SAR["frequency_band"]
    sar.instrument_mode = c.SENTINEL_GRD_SAR["instrument_mode"]
    sar.center_frequency = c.SENTINEL_GRD_SAR["center_frequency"]
    sar.resolution_range = c.SENTINEL_GRD_SAR["resolution_range"]
    sar.resolution_azimuth = c.SENTINEL_GRD_SAR["resolution_azimuth"]
    sar.pixel_spacing_range = c.SENTINEL_GRD_SAR["pixel_spacing_range"]
    sar.observation_direction = c.SENTINEL_GRD_SAR["observation_direction"]
    sar.pixel_spacing_azimuth = c.SENTINEL_GRD_SAR["pixel_spacing_azimuth"]
    sar.looks_equivalent_number = c.SENTINEL_GRD_SAR["looks_equivalent_number"]

    # Satellite Extension
    sat = SatExtension.summaries(collection, add_if_missing=True)
    sat.orbit_state = c.SENTINEL_GRD_SAT["orbit_state"]

    # Item Asset Extension
    assets = ItemAssetsExtension.ext(collection, add_if_missing=True)
    assets.item_assets = c.SENTINEL_GRD_ASSETS

    return collection


def create_item(
    granule_href: str,
    read_href_modifier: Optional[ReadHrefModifier] = None,
    archive_format: Format = Format.SAFE,
    **kwargs: Any,
) -> pystac.Item:
    """Create a STC Item from a Sentinel-1 GRD scene.

    Args:
        granule_href (str): The HREF to the granule.
            This is expected to be a path to a SAFE archive (see format for other options).
        read_href_modifier: A function that takes an HREF and returns a modified HREF.
            This can be used to modify a HREF to make it readable, e.g. appending
            an Azure SAS token or creating a signed URL.
        archive_format: An enum specifying the format of the granule. Currently supported formats
            are SAFE (default) and COG.


    Returns:
        pystac.Item: An item representing the Sentinel-1 GRD scene.
    """

    metalinks = MetadataLinks(
        granule_href,
        read_href_modifier,
        archive_format,
        **kwargs,
    )

    product_metadata = GRDProductMetadata(
        metalinks.product_metadata_href,
        metalinks.grouped_hrefs,
        metalinks.map_filename,
        metalinks.manifest,
    )

    scene_id = product_metadata.scene_id

    # Remove the last segment of the scene id so the same scene reprocessed
    # at different times will have the same Item ID
    item_id = scene_id[:-5]

    item = pystac.Item(
        id=item_id,
        geometry=product_metadata.geometry,
        bbox=product_metadata.bbox,
        datetime=product_metadata.get_datetime,
        properties={},
        stac_extensions=[],
    )

    # ---- Add Extensions ----
    # SAR Extension
    sar = SarExtension.ext(item, add_if_missing=True)
    fill_sar_properties(sar, metalinks.manifest, product_metadata.resolution)

    # Satellite Extension
    sat = SatExtension.ext(item, add_if_missing=True)
    fill_sat_properties(sat, metalinks.manifest)

    # eo
    EOExtension.ext(item, add_if_missing=True)

    # Projection Extension
    projection = ProjectionExtension.ext(item, add_if_missing=True)
    projection.epsg = 4326
    projection.bbox = product_metadata.bbox
    shape = get_shape(metalinks, read_href_modifier, **kwargs)
    projection.shape = shape
    projection.transform = transform_from_bbox(projection.bbox, shape)
    centroid = shapely.geometry.shape(item.geometry).centroid
    projection.centroid = {"lat": round(centroid.y, 5), "lon": round(centroid.x, 5)}

    # --Common metadata--
    item.common_metadata.providers = [c.SENTINEL_PROVIDER]
    item.common_metadata.platform = (
        product_metadata.platform.lower()
        if product_metadata.platform
        else product_metadata.platform
    )
    item.common_metadata.constellation = c.SENTINEL_CONSTELLATION

    # Add s1 properties
    item.properties.update(product_metadata.metadata_dict)

    item.properties["s1:shape"] = shape
    item.properties["s1:product_identifier"] = scene_id

    if pdt := metalinks.manifest.find_attr(
        "stop", ".//safe:processing[@name='GRD Post Processing']"
    ):
        item.properties["s1:processing_datetime"] = f"{pdt}Z"

    # Add assets to item
    item.add_asset(*metalinks.create_manifest_asset())

    # Annotations for bands
    for asset_obj in metalinks.create_product_asset():
        item.add_asset(asset_obj[0], asset_obj[1])

    # Calibrations for bands
    for asset_obj in metalinks.create_calibration_asset():
        item.add_asset(asset_obj[0], asset_obj[1])

    # Noise for bands
    for asset_obj in metalinks.create_noise_asset():
        item.add_asset(asset_obj[0], asset_obj[1])

    # Thumbnail
    if metalinks.thumbnail_href is not None:
        desc = (
            "An averaged, decimated preview image in PNG format. Single polarization "
            "products are represented with a grey scale image. Dual polarization products "
            "are represented by a single composite colour image in RGB with the red channel "
            "(R) representing the  co-polarization VV or HH), the green channel (G) "
            "represents the cross-polarization (VH or HV) and the blue channel (B) "
            "represents the ratio of the cross an co-polarizations."
        )
        item.add_asset(
            "thumbnail",
            pystac.Asset(
                href=metalinks.thumbnail_href,
                media_type=pystac.MediaType.PNG,
                roles=["thumbnail"],
                title="Preview Image",
                description=desc,
            ),
        )

    images_media_type = None
    if archive_format == Format.SAFE:
        images_media_type = pystac.MediaType.GEOTIFF
    elif archive_format == Format.COG:
        images_media_type = pystac.MediaType.COG

    image_assets = dict(
        [
            image_asset_from_href(
                os.path.join(granule_href, image_path),
                item,
                media_type=images_media_type,
            )
            for image_path in product_metadata.image_paths
        ]
    )

    for key, asset in image_assets.items():
        assert key not in item.assets
        item.add_asset(key, asset)

    # --Links--
    item.links.append(c.SENTINEL_GRD_LICENSE)
    item.links.append(c.SENTINEL_GRD_TECHNICAL_GUIDE)

    return item
