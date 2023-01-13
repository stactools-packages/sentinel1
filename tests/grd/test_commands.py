from pathlib import Path

# import pystac
from pystac import Collection, Item

from tests import run_command, test_data


def test_create_collection(tmp_path: Path) -> None:
    destination = tmp_path / "sentinel1-grd.json"
    result = run_command(f"sentinel1 grd create-collection {tmp_path}")
    assert result.exit_code == 0, "\n{}".format(result.output)
    paths = [p for p in tmp_path.iterdir() if p.suffix == ".json"]
    assert len(paths) == 1
    collection = Collection.from_file(str(destination))
    assert collection.id == "sentinel1-grd"
    collection.set_self_href(
        str(destination)
    )  # Must set the self reference to pass validation
    collection.validate()


def test_create_items(tmp_path: Path) -> None:
    item_id = "S1A_EW_GRDM_1SDH_20221130T014342_20221130T014446_046117_058549_BB15"

    infile = test_data.get_path(f"data-files/grd/{item_id}")
    result = run_command(f"sentinel1 grd create-item {infile} {tmp_path} --format COG")
    assert result.exit_code == 0, "\n{}".format(result.output)

    paths = [p for p in tmp_path.iterdir() if p.suffix == ".json"]
    assert len(paths) == 1

    item = Item.from_file(str(tmp_path / paths[0]))
    item.validate()
