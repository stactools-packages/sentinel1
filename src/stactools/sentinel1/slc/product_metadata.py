from typing import Any, Dict

from pystac.utils import datetime_to_str

from ..product_metadata import ProductMetadata


class SLCProductMetadata(ProductMetadata):
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
            "s1:orbit_source": self.orbit_source(),
            "s1:slice_number": self._root.find_text(".//s1sarl1:sliceNumber"),
            "s1:total_slices": self._root.find_text(".//s1sarl1:totalSlices"),
            "s1:swaths": [elem.text for elem in self._root.findall(".//s1sarl1:swath")],
        }

        return {k: v for k, v in result.items() if v is not None}
