from unittest import TestCase

import pystac
from pystac.extensions.eo import EOExtension
from pystac.utils import is_absolute_href

from stactools.sentinel1.grd import Format, stac
from stactools.sentinel1.grd.constants import SENTINEL_POLARIZATIONS
from tests import test_data


class StacTest(TestCase):
    def test_create_collection(self) -> None:
        collection = stac.create_collection("")
        assert isinstance(collection, pystac.Collection)

    def test_validate_collection(self) -> None:
        collection = stac.create_collection("")
        collection.normalize_hrefs("./")
        collection.validate()

    def test_create_item(self) -> None:
        item_id = "S1A_IW_GRDH_1SDV_20210809T173953_20210809T174018_039156_049F13_6FF8"
        granule_href = test_data.get_path(
            "data-files/grd/S1A_IW_GRDH_1SDV_20210809T173953_20210809T174018_039156_049F13_6FF8.SAFE"  # noqa
        )
        item = stac.create_item(granule_href, archive_format=Format.SAFE)

        item.validate()

        self.assertEqual(item.id, item_id)

        bands_seen = set()

        for _, asset in item.assets.items():
            # Ensure that there's no relative path parts
            # in the asset HREFs
            self.assertTrue("/./" not in asset.href)
            self.assertTrue(is_absolute_href(asset.href))
            asset_eo = EOExtension.ext(asset)
            bands = asset_eo.bands
            if bands is not None:
                bands_seen |= set(b.name for b in bands)

        # TODO: Verify the intent of this test
        # The prior test was in a List Comprehension which doesn't evaluate to a return
        for x in bands_seen:
            self.assertTrue(x.lower() in list(SENTINEL_POLARIZATIONS.keys()))
