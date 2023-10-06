from typing import Any, Callable, Dict, List

from pystac.utils import datetime_to_str
from stactools.core.io.xml import XmlElement

from ..product_metadata import ProductMetadata


class SLCProductMetadata(ProductMetadata):
    def __init__(
        self,
        href: str,
        file_hrefs: Dict[str, List[str]],
        file_mapper: Callable[[str], str],
        manifest: XmlElement,
    ) -> None:
        super().__init__(href, file_hrefs, file_mapper, manifest)
        # self.resolution = self.product_id.split("_")[2][-1]

    @property
    def metadata_dict(self) -> Dict[str, Any]:
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
            # "s1:processing_level": self.product_id.split("_")[3][0],
            # "s1:resolution": resolutions[self.resolution],
            "s1:orbit_source": self.orbit_source(),
            "s1:slice_number": self._root.find_text(".//s1sarl1:sliceNumber"),
            "s1:total_slices": self._root.find_text(".//s1sarl1:totalSlices"),
            "s1:swaths": [elem.text for elem in self._root.findall(".//s1sarl1:swath")],
            # "s1:frame_number": get_frame_number(root),
            # "s1:stop_anxtime": get_stop_anxtime(root),
        }


        return {k: v for k, v in result.items() if v is not None}
