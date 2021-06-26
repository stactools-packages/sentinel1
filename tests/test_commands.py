import os
from tempfile import TemporaryDirectory

import pystac
from pystac.utils import is_absolute_href
from stactools.sentinel1 import stac
from stactools.sentinel1.commands import create_sentinel1_command
from stactools.testing import CliTestCase
from tests import test_data


class CreateItemTest(CliTestCase):
    def create_subcommand_functions(self):
        return [create_sentinel1_command]

    def test_create_item(self):
        item = stac.create_item(
            test_data.get_path('data-files/S1A_20200103_17RMJ_ASC'),
            asset='Gamma0_VV.vrt',
            include_grd_metadata=True)
        assert isinstance(item, pystac.item.Item)

    def test_create_item_network(self):
        ''' read from AWS public bucket'''
        bucket = 'sentinel-s1-rtc-indigo'
        key = 'tiles/RTC/1/IW/17/R/MJ/2020/S1A_20200103_17RMJ_ASC'
        item = stac.create_item(f's3://{bucket}/{key}')
        assert isinstance(item, pystac.item.Item)

    def test_create_collection(self):
        collection = stac.create_collection()
        assert isinstance(collection, pystac.collection.Collection)

    def test_validate_collection(self):
        collection = stac.create_collection()
        collection.normalize_hrefs('./')
        collection.validate()

    def test_create_catalog(self):
        ''' create, save, open, and validate a STAC '''
        collection = stac.create_collection()
        item1 = stac.create_item(
            test_data.get_path('data-files/S1B_20161121_12SYJ_ASC'),
            asset='local_incident_angle.vrt')
        item2 = stac.create_item(
            test_data.get_path('data-files/S1A_20200103_17RMJ_ASC'),
            asset='local_incident_angle.vrt')
        collection.add_items([item1, item2])

        with TemporaryDirectory() as tmp_dir:
            collection.generate_subcatalogs(template='${year}')
            collection.normalize_hrefs(tmp_dir)
            # CatalogType.SELF_CONTAINED or CatalogType.ABSOLUTE_PUBLISHED
            collection.save(catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED)
            collection = pystac.read_file(
                os.path.join(tmp_dir, 'collection.json'))
            collection.validate()

    def test_cli_create_item(self):
        granule_hrefs = [
            test_data.get_path(f'data-files/{x}') for x in [
                'S1B_20161121_12SYJ_ASC',
            ]
        ]

        for granule_href in granule_hrefs:
            with self.subTest(granule_href):
                with TemporaryDirectory() as tmp_dir:
                    cmd = [
                        'sentinel1', 'create-item', granule_href, tmp_dir,
                        '-a', 'local_incident_angle.vrt'
                    ]
                    self.run_command(cmd)

                    jsons = [
                        p for p in os.listdir(tmp_dir) if p.endswith('.json')
                    ]
                    self.assertEqual(len(jsons), 1)

                    for fname in jsons:
                        item = pystac.read_file(os.path.join(tmp_dir, fname))

                        item.validate()

                        for asset in item.assets.values():
                            self.assertTrue(is_absolute_href(asset.href))
