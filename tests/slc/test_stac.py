from itertools import product

import pystac
from pystac.extensions.eo import EOExtension
from pystac.utils import is_absolute_href

from stactools.sentinel1.formats import Format
from stactools.sentinel1.slc import constants as c
from stactools.sentinel1.slc import stac
from stactools.sentinel1.slc.constants import SENTINEL_POLARIZATIONS
from tests import test_data


def test_create_collection() -> None:
    collection = stac.create_collection("")
    assert isinstance(collection, pystac.Collection)


def test_validate_collection() -> None:
    collection = stac.create_collection("")
    collection.normalize_hrefs("./")
    collection.validate()


def test_create_item() -> None:
    product_identifier = (
        "S1A_IW_SL1__1_SH_20141031T095929_20141031T100002_003072_003842_91FC"
    )
    granule_href = test_data.get_path(
        "data-files/slc/S1A_IW_SL1__1_SH_20141031T095929_20141031T100002_003072_003842_91FC.SAFE"  # noqa
    )
    item = stac.create_item(granule_href, archive_format=Format.SAFE)

    item.validate()

    assert item.id == product_identifier[:-5]

    bands_seen = set()

    for _, asset in item.assets.items():
        # Ensure that there's no relative path parts
        # in the asset HREFs
        assert "/./" not in asset.href
        assert is_absolute_href(asset.href)
        asset_eo = EOExtension.ext(asset)
        bands = asset_eo.bands
        if bands is not None:
            bands_seen |= set(b.name for b in bands)

    # TODO: Verify the intent of this test
    # The prior test was in a List Comprehension which doesn't evaluate to a return
    for x in bands_seen:
        assert x.lower() in list(SENTINEL_POLARIZATIONS.keys())

    assert item.properties.get("start_datetime") == "2014-10-31T09:59:31.293840Z"
    assert item.properties.get("end_datetime") == "2014-10-31T09:59:58.717016Z"

    assert item.properties.get("constellation") == c.SENTINEL_CONSTELLATION
    assert item.properties.get("platform") == "sentinel-1a"

    assert item.properties.get("proj:code") == "EPSG:4326"
    assert item.properties.get("proj:bbox") == [
        -53.661625,
        69.582458,
        -45.827332,
        71.715393,
    ]
    assert item.properties.get("proj:shape") == [21032, 14733]
    assert item.properties.get("proj:transform") == [
        0.0005317513744654858,
        0.0,
        -53.661625,
        0.0,
        -0.00010141379802206178,
        71.715393,
    ]

    assert item.properties.get("proj:centroid") == {
        "lat": 70.65156,
        "lon": -49.86285,
    }

    # Test polarisation added to item-asset schemas titles
    swaths = ["IW1", "IW2", "IW3"]
    polarisations = ["HH"]
    asset_types = ["schema-calibration", "schema-noise", "schema-product"]
    for swath, polarisation, asset_type in product(swaths, polarisations, asset_types):
        asset_key = f"{asset_type}-{swath.lower()}-{polarisation.lower()}"
        title_prefix = f"{swath.upper()} {polarisation.upper()}"
        if asset_key in item.assets:
            asset_title = item.assets[asset_key].title
            if asset_title:
                assert title_prefix == asset_title[: len(title_prefix)]

    assert item.properties.get("s1:product_identifier") == product_identifier
    assert (
        item.properties.get("s1:processing_datetime") == "2014-10-31T20:34:21.000000Z"
    )
