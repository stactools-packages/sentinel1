import pystac
from pystac.extensions.eo import EOExtension
from pystac.utils import is_absolute_href

from stactools.sentinel1.grd import Format, stac
from stactools.sentinel1.grd.constants import SENTINEL_POLARIZATIONS
from tests import test_data


def test_create_collection() -> None:
    collection = stac.create_collection("")
    assert isinstance(collection, pystac.Collection)


def test_validate_collection() -> None:
    collection = stac.create_collection("")
    collection.normalize_hrefs("./")
    collection.validate()


def test_create_item() -> None:
    item_id = "S1A_IW_GRDH_1SDV_20210809T173953_20210809T174018_039156_049F13_6FF8"
    granule_href = test_data.get_path(
        "data-files/grd/S1A_IW_GRDH_1SDV_20210809T173953_20210809T174018_039156_049F13_6FF8.SAFE"  # noqa
    )
    item = stac.create_item(granule_href, archive_format=Format.SAFE)

    item.validate()

    assert item.id == item_id

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

    assert item.properties.get("start_datetime") == "2021-08-09T17:39:53.153776Z"
    assert item.properties.get("end_datetime") == "2021-08-09T17:40:18.152800Z"

    # Test polarisation added to item-asset schemas titles
    polarisations = ["HH", "HV", "VV", "VH"]
    asset_types = ["schema-calibration", "schema-noise", "schema-product"]
    for polarisation in polarisations:
        for asset_type in asset_types:
            asset_key = f"{asset_type}-{polarisation.lower()}"
            if asset_key in item.assets:
                asset_title = item.assets[asset_key].title
                if asset_title:
                    assert polarisation == asset_title[: len(polarisation)]
