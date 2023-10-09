import unittest

import pystac
from pystac.extensions.sar import SarExtension
from pystac.extensions.sat import SatExtension

from stactools.sentinel1.metadata_links import MetadataLinks
from stactools.sentinel1.slc.product_metadata import SLCProductMetadata
from stactools.sentinel1.slc.properties import (
    fill_common_sar_properties,
    fill_sat_properties,
)
from tests import test_data


class Sentinel1MetadataTest(unittest.TestCase):
    def test_parses_product_metadata_properties(self) -> None:

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/slc/S1A_IW_SL1__1_SH_20141031T095929_20141031T100002_003072_003842_91FC.SAFE"  # noqa
        )

        metalinks = MetadataLinks(manifest_path)

        product_metadata = SLCProductMetadata(
            metalinks.product_metadata_href,
            metalinks.grouped_hrefs,
            metalinks.map_filename,
            metalinks.manifest,
        )

        item = pystac.Item(
            id=product_metadata.scene_id,
            geometry=product_metadata.geometry,
            bbox=product_metadata.bbox,
            datetime=product_metadata.get_datetime,
            properties={},
            stac_extensions=[],
        )

        # ---- Add Extensions ----
        # sar
        sar = SarExtension.ext(item, add_if_missing=True)
        fill_common_sar_properties(sar, metalinks.manifest)

        # sat
        sat = SatExtension.ext(item, add_if_missing=True)
        fill_sat_properties(sat, metalinks.manifest)

        # Make a dictionary of the properties
        # TODO: test more of the properties
        properties_actual = {
            "bbox": item.bbox,
            "sar_band": item.properties["sar:frequency_band"],
            "centre_frequency": item.properties["sar:center_frequency"],
            "polarizations": item.properties["sar:polarizations"],
            "product_type": item.properties["sar:product_type"],
        }

        properties_expected = {
            "bbox": [-53.661625, 69.582458, -45.827332, 71.715393],
            "sar_band": "C",
            "centre_frequency": 5.405,
            "polarizations": ["HH"],
            "product_type": "SLC",
        }

        for k, v in properties_expected.items():
            self.assertIn(k, properties_actual)
            self.assertEqual(properties_actual[k], v)
