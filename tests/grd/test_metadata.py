import unittest

import pystac
from pystac.extensions.sar import SarExtension
from pystac.extensions.sat import SatExtension

from stactools.sentinel1.grd.metadata_links import MetadataLinks
from stactools.sentinel1.grd.product_metadata import ProductMetadata
from stactools.sentinel1.grd.properties import (fill_sar_properties,
                                                fill_sat_properties)
from tests import test_data


class Sentinel1MetadataTest(unittest.TestCase):

    def test_parses_product_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/grd/S1A_IW_GRDH_1SDV_20210809T173953_20210809T174018_039156_049F13_6FF8.SAFE"  # noqa
        )

        metalinks = MetadataLinks(manifest_path)

        product_metadata = ProductMetadata(metalinks.product_metadata_href,
                                           metalinks.grouped_hrefs,
                                           metalinks.map_filename,
                                           metalinks.manifest)

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
        fill_sar_properties(sar, metalinks.manifest,
                            product_metadata.resolution)

        # sat
        sat = SatExtension.ext(item, add_if_missing=True)
        fill_sat_properties(sat, metalinks.manifest)

        # Make a dictionary of the properties
        # TODO: test more of the properties
        s1_props = {
            "bbox": item.bbox,
            "sar_band": item.properties["sar:frequency_band"],
            "centre_frequency": item.properties["sar:center_frequency"],
            "polarizations": item.properties["sar:polarizations"],
            "product_type": item.properties["sar:product_type"]
        }

        expected = {
            "bbox": (1.512143, 44.536255, 5.188996, 46.436539),
            "sar_band": "C",
            "centre_frequency": 5.405,
            "polarizations": ["VV", "VH"],
            "product_type": "GRD"
        }

        for k, v in expected.items():
            self.assertIn(k, s1_props)
            self.assertEqual(s1_props[k], v)
