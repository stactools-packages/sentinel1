import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Tuple

import numpy as np
import pystac
import rasterio
import rasterio.features
from pystac.extensions.raster import DataType, Sampling, Statistics
from pystac.utils import str_to_datetime
from rasterio import Affine as A
from rasterio.warp import transform_geom
from shapely.geometry import mapping, shape

logger = logging.getLogger(__name__)


class RTCMetadata:
    def __init__(self, href: str, asset: str) -> None:
        self.href = href
        self.asset = asset

        def _load_metadata_from_asset(
            scale: int = 1, precision: int = 5
        ) -> Tuple[Dict[str, Any], List[float], Dict[str, Any]]:
            """key metadata stored in Geotiff tags"""
            with rasterio.Env(
                AWS_NO_SIGN_REQUEST="YES", GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"
            ):
                with rasterio.open(os.path.join(href, self.asset)) as src:
                    metadata = src.profile
                    metadata.update(src.tags())
                    metadata["SHAPE"] = src.shape

                    bbox, footprint = _get_geometries(src, scale, precision)

            return metadata, bbox, footprint

        def _get_geometries(
            src: Any, scale: int, precision: int
        ) -> Tuple[List[float], Dict[str, Any]]:
            """scale can be 1,2,4,8,16. scale=1 creates most precise footprint
            at the expense of reading all pixel values. scale=2 reads 1/4 amount
            of data be overestimates footprint by at least 1pixel (20 meters).
            """
            with rasterio.vrt.WarpedVRT(src, crs="EPSG:4326") as vrt:
                bbox = [np.round(x, decimals=precision) for x in vrt.bounds]
            arr = src.read(1, out_shape=(src.height // scale, src.width // scale))
            arr[np.where(arr != 0)] = 1
            transform = src.transform * A.scale(scale)

            # Get polygon covering entire valid data region
            rioshapes = rasterio.features.shapes(arr, transform=transform)
            max_perimeter = 0
            max_geometry = None
            for geom, val in rioshapes:
                if val == 1:
                    geometry = shape(geom)
                    if geometry.length > max_perimeter:
                        max_perimeter = geometry.length
                        max_geometry = geometry
            if max_geometry is None:
                raise ValueError("No valid footprint could be calculated")
            valid_geom = mapping(max_geometry.convex_hull)
            footprint = transform_geom(
                src.crs, "EPSG:4326", valid_geom, precision=precision
            )

            return bbox, footprint

        def _get_provenance() -> List[str]:
            """RTC products are from mosaiced GRD frames"""
            # NOTE: just GRD frame names? or additional info, like IPF from manifest.safe
            # <safe:software name="Sentinel-1 IPF" version="002.72"/>
            grd_ids = []
            for i in range(1, int(self.metadata["NUMBER_SCENES"]) + 1):
                m = json.loads(self.metadata[f"SCENE_{i}_METADATA"])
                grd_ids.append(m["title"])

            return grd_ids

        def _get_times() -> Tuple[datetime, datetime, datetime]:
            """UTC start and end times of GRDs used in RTC product"""
            times = []
            for i in range(1, int(self.metadata["NUMBER_SCENES"]) + 1):
                m = json.loads(self.metadata[f"SCENE_{i}_METADATA"])
                times += [m["start_time"], m["end_time"]]
                start = str_to_datetime(min(times))
                end = str_to_datetime(max(times))
                mid = start + (end - start) / 2
                mid = mid.replace(microsecond=0)
            return start, mid, end

        self.metadata, self.bbox, self.geometry = _load_metadata_from_asset()
        self.grd_ids = _get_provenance()
        self.start_datetime, self.datetime, self.end_datetime = _get_times()

    @property
    def product_id(self) -> str:
        date = self.metadata["DATE"].replace("-", "")
        orbNames = {"ascending": "ASC", "descending": "DSC"}
        orb = orbNames[self.metadata["ORBIT_DIRECTION"]]
        id = f"{self.metadata['MISSION_ID']}_{date}_{self.metadata['TILE_ID']}_{orb}"
        return id

    @property
    def image_media_type(self) -> str:
        return pystac.MediaType.COG

    @property
    def shape(self) -> List[int]:
        return list(self.metadata["SHAPE"])

    @property
    def image_paths(self) -> List[str]:
        return ["Gamma0_VV.tif", "Gamma0_VH.tif", "local_incident_angle.tif"]

    @property
    def absolute_orbit(self) -> int:
        return int(self.metadata["ABSOLUTE_ORBIT_NUMBER"])

    @property
    def relative_orbit(self) -> int:
        """https://forum.step.esa.int/t/sentinel-1-relative-orbit-from-filename/7042"""
        satellite_lookup = {"S1B": 27, "S1A": 73}
        modifier = satellite_lookup[self.metadata["MISSION_ID"]]
        rel_orbit = ((self.absolute_orbit - modifier) % 175) + 1
        return rel_orbit

    @property
    def orbit_state(self) -> str:
        return str(self.metadata["ORBIT_DIRECTION"])

    @property
    def platform(self) -> str:
        platformMap = dict(S1A="sentinel-1a", S1B="sentinel-1b")
        return platformMap[self.metadata["MISSION_ID"]]

    @property
    def epsg(self) -> int:
        return int(self.metadata["crs"].to_epsg())

    @property
    def valid_percent(self) -> float:
        # Common to 3 assets of RTC item
        return float(self.metadata["VALID_PIXEL_PERCENT"])

    @property
    def metadata_dict(self) -> Dict[str, Any]:
        """match s2 l2a cogs from https://earth-search.aws.element84.com/v0"""
        sentinel_metadata = {
            # NOTE: once PySTAC adds MGRS extension can move this to stac.py
            "mgrs:utm_zone": self.metadata["TILE_ID"][:2],
            "mgrs:latitude_band": self.metadata["TILE_ID"][2],
            "mgrs:grid_square": self.metadata["TILE_ID"][3:],
            "sentinel:mgrs": self.metadata["TILE_ID"],
            "sentinel:product_ids": self.grd_ids,
        }
        return sentinel_metadata

    @property
    def asset_dict(self) -> Dict[str, Any]:
        """map image_path (geotif) to pystac.Asset fields"""
        asset_dict = {
            "Gamma0_VV.tif": dict(
                key="gamma0_vv",
                title="Gamma0 VV backscatter",
                roles=["data", "gamma0"],
                raster=dict(
                    nodata=0,
                    sampling=Sampling.AREA,
                    data_type=DataType.FLOAT32,
                    statistics=Statistics({"valid_percent": self.valid_percent}),
                ),
            ),
            "Gamma0_VH.tif": dict(
                key="gamma0_vh",
                title="Gamma0 VH backscatter",
                roles=["data", "gamma0"],
                raster=dict(
                    nodata=0,
                    sampling=Sampling.AREA,
                    data_type=DataType.FLOAT32,
                    statistics=Statistics({"valid_percent": self.valid_percent}),
                ),
            ),
            "local_incident_angle.tif": dict(
                key="incidence",
                title="Local incidence angle",
                roles=["data", "local-incidence-angle"],
                raster=dict(
                    nodata=0,
                    sampling=Sampling.AREA,
                    data_type=DataType.UINT16,
                    unit="degrees",
                    scale=0.01,
                    statistics=Statistics({"valid_percent": self.valid_percent}),
                ),
            ),
        }

        return asset_dict
