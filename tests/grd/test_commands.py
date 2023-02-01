import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable, List

import pystac
from click import Command, Group
from pystac.extensions.eo import EOExtension
from pystac.utils import is_absolute_href
from stactools.testing.cli_test import CliTestCase

from stactools.sentinel1.commands import create_sentinel1_command
from stactools.sentinel1.grd.constants import SENTINEL_POLARIZATIONS
from tests import test_data


class CreateItemTest(CliTestCase):
    def create_subcommand_functions(self) -> List[Callable[[Group], Command]]:
        return [create_sentinel1_command]

    def test_create_collection(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            destination = tmp_path / "sentinel1-grd.json"
            cmd = ["sentinel1", "grd", "create-collection", f"{tmp_path}"]
            result = self.run_command(cmd)

            assert result.exit_code == 0, "\n{}".format(result.output)
            paths = [p for p in tmp_path.iterdir() if p.suffix == ".json"]

            assert len(paths) == 1
            collection = pystac.Collection.from_file(str(destination))

            assert collection.id == "sentinel1-grd"
            # collection.set_self_href(
            #    str(destination)
            # )  # Must set the self reference to pass validation
            collection.validate()

    def test_create_item(self) -> None:
        item_id = "S1A_IW_GRDH_1SDV_20210809T173953_20210809T174018_039156_049F13_6FF8"
        granule_href = test_data.get_path(
            "data-files/grd/S1A_IW_GRDH_1SDV_20210809T173953_20210809T174018_039156_049F13_6FF8.SAFE"  # noqa
        )

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel1", "grd", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

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

                for x in bands_seen:
                    self.assertTrue(x.lower() in list(SENTINEL_POLARIZATIONS.keys()))
