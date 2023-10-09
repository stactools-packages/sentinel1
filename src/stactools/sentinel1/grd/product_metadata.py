from typing import Any, Callable, Dict, List

from pystac.utils import datetime_to_str
from stactools.core.io.xml import XmlElement

from ..product_metadata import ProductMetadata


class GRDProductMetadata(ProductMetadata):
    def __init__(
        self,
        href: str,
        file_hrefs: Dict[str, List[str]],
        file_mapper: Callable[[str], str],
        manifest: XmlElement,
    ) -> None:
        super().__init__(href, file_hrefs, file_mapper, manifest)
        self.resolution = self.product_id.split("_")[2][-1]

    @property
    def metadata_dict(self) -> Dict[str, Any]:

        resolutions = {"F": "full", "H": "high", "M": "medium"}

        tmp = self._root.find(".//s1sarl1:sliceNumber")
        slice_number = tmp.text if tmp is not None else None
        tmp = self._root.find(".//s1sarl1:totalSlices")
        total_slices = tmp.text if tmp is not None else None

        result = {
            "start_datetime": datetime_to_str(self.start_datetime),
            "end_datetime": datetime_to_str(self.end_datetime),
            "s1:instrument_configuration_ID": self._root.find_text(
                ".//s1sarl1:instrumentConfigurationID"
            ),
            "s1:datatake_id": self._root.find_text(".//s1sarl1:missionDataTakeID"),
            "s1:product_timeliness": self._root.find_text(
                ".//s1sarl1:productTimelinessCategory"
            ),
            "s1:processing_level": self.product_id.split("_")[3][0],
            "s1:resolution": resolutions[self.resolution],
            "s1:orbit_source": self.orbit_source(),
            "s1:slice_number": slice_number,
            "s1:total_slices": total_slices,
        }

        return {k: v for k, v in result.items() if v is not None}
