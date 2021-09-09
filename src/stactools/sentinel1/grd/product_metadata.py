import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from pystac.utils import str_to_datetime
from shapely.geometry import Polygon, mapping  # type: ignore
from stactools.core.io.xml import XmlElement


class ProductMetadataError(Exception):
    pass


class ProductMetadata:
    def __init__(
        self,
        href,
    ) -> None:
        self.href = href
        self._root = XmlElement.from_file(href)

        def _get_geometries():
            # Find the footprint descriptor
            footprint_text = self._root.findall(".//gml:coordinates")
            if footprint_text is None:
                ProductMetadataError(
                    f"Cannot parse footprint from product metadata at {self.href}"
                )
            # Convert to values
            footprint_value = [
                float(x)
                for x in footprint_text[0].text.replace(" ", ",").split(",")
            ]

            footprint_points = [
                p[::-1] for p in list(zip(*[iter(footprint_value)] * 2))
            ]

            footprint_polygon = Polygon(footprint_points)
            geometry = mapping(footprint_polygon)
            bbox = footprint_polygon.bounds

            return (bbox, geometry)

        self.bbox, self.geometry = _get_geometries()

    @property
    def scene_id(self) -> str:
        """Returns the string to be used for a STAC Item id.

        Removes the processing number and .SAFE extension
        from the product_id defined below.

        Parsed based on the naming convention found here:
        https://sentinel.esa.int/web/sentinel/user-guides/sentinel-2-msi/naming-convention
        """
        scene_id = self.product_id.split(".")[0]

        return scene_id

    @property
    def product_id(self) -> str:
        # Parse the name from href as it doesn't exist in xml files
        href = self.href
        result = href.split("/")[-2]
        if result is None:
            raise ValueError(
                "Cannot determine product ID using product metadata "
                f"at {self.href}")
        else:
            return result

    @property
    def get_datetime(self) -> datetime:
        start_time = self._root.findall(".//safe:startTime")[0].text
        end_time = self._root.findall(".//safe:stopTime")[0].text

        central_time = (
            datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%f") +
            (datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S.%f") -
             datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%f")) / 2)

        if central_time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.href}")
        else:
            return str_to_datetime(str(central_time))

    @property
    def start_datetime(self) -> datetime:
        time = self._root.findall(".//safe:startTime")

        if time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.href}")
        else:
            return str_to_datetime(f"{time[0].text}Z")

    @property
    def end_datetime(self) -> datetime:
        time = self._root.findall(".//safe:stopTime")

        if time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.href}")
        else:
            return str_to_datetime(f"{time[0].text}Z")

    @property
    def platform(self) -> Optional[str]:

        family_name = self._root.findall(".//safe:familyName")[0].text
        platform_name = self._root.findall(".//safe:number")[0].text

        return family_name + platform_name

    @property
    def cycle_number(self) -> Optional[str]:

        return self._root.findall(".//safe:cycleNumber")[0].text

    @property
    def image_paths(self) -> List[str]:
        head_folder = os.path.dirname(self.href)
        measurements = os.path.join(head_folder, "measurement")
        return [x for x in os.listdir(measurements) if x.endswith("tiff")]

    @property
    def metadata_dict(self) -> Dict[str, Any]:
        result = {
            "start_datetime":
            str(self.start_datetime),
            "end_datetime":
            str(self.end_datetime),
            "s1:instrument_configuration_ID":
            self._root.findall(".//s1sarl1:instrumentConfigurationID")[0].text,
            "s1:datatake_id":
            self._root.findall(".//s1sarl1:missionDataTakeID")[0].text,
        }

        return {k: v for k, v in result.items() if v is not None}
