#!/usr/bin/env python3
"""
Generate example STAC from test data
"""
import shutil
from pathlib import Path

import pystac

from stactools.sentinel1.formats import Format
from stactools.sentinel1.grd import stac as grd
from stactools.sentinel1.rtc import stac as rtc

# GRD generate examples
root = Path(__file__).parents[1]
examples = root / "examples"
grd_data = root / "tests" / "data-files" / "grd"

shutil.rmtree(examples, ignore_errors=True)

grd_collection = grd.create_collection(str(examples / "grd" / "collection.json"))

item1 = grd.create_item(
    str(
        grd_data / "S1A_EW_GRDM_1SDH_20221130T014342_20221130T014446_046117_058549_BB15"
    ),
    archive_format=Format.COG,
)
item2 = grd.create_item(
    str(
        grd_data
        / "S1A_IW_GRDH_1SDV_20210809T173953_20210809T174018_039156_049F13_6FF8.SAFE"
    ),
    archive_format=Format.SAFE,
)
grd_collection.add_items([item1, item2])

grd_collection.normalize_hrefs(str(examples / "grd"))
grd_collection.make_all_asset_hrefs_relative()
grd_collection.validate_all()
grd_collection.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

# RTC generate examples
catalog = pystac.Catalog(
    id="sentinel1-rtc-example",
    description=(
        "Example Catalog: Analysis Ready Sentinel-1 "
        "Backscatter Imagery AWS Public Dataset"
    ),
    title="Sentinel-1 RTC AWS Open Data",
)

collection = rtc.create_collection()

base_href = "https://sentinel-s1-rtc-indigo.s3.us-west-2.amazonaws.com"
key = "tiles/RTC/1/IW/17/R/MJ/2020/S1A_20200103_17RMJ_ASC"
item1 = rtc.create_item(f"{base_href}/{key}")

key = "tiles/RTC/1/IW/12/S/YJ/2016/S1B_20161121_12SYJ_ASC"
item2 = rtc.create_item(f"{base_href}/{key}")

collection.add_items([item1, item2])

catalog.add_child(collection)
catalog.generate_subcatalogs(template="${year}")
catalog.normalize_hrefs(str(examples / "rtc"))
catalog.make_all_asset_hrefs_relative()
catalog.validate_all()
catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
