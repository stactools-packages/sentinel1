from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from pystac.utils import str_to_datetime
from shapely.geometry import Polygon, mapping  # type: ignore
from stactools.core.io import ReadHrefModifier
from stactools.core.io.xml import XmlElement

from stactools.sentinel1.grd.metadata_links import MetadataLinks


class ProductMetadataError(Exception):
    pass


def get_shape(meta_links: MetadataLinks,
              read_href_modifier: Optional[ReadHrefModifier]) -> List[int]:
    links = meta_links.create_product_asset()
    root = XmlElement.from_file(links[0][1].href, read_href_modifier)

    x_size = int(root.findall(".//numberOfSamples")[0].text)
    y_size = int(root.findall(".//numberOfLines")[0].text)

    return [x_size, y_size]


class ProductMetadata:
    def __init__(
        self,
        href,
        file_hrefs: Dict[str, List[str]],
        file_mapper: Callable[[str], str],
        read_href_modifier: Optional[ReadHrefModifier] = None,
    ) -> None:
        self.href = href
        self._root = XmlElement.from_file(href, read_href_modifier)
        self.file_hrefs = file_hrefs
        self.file_mapper = file_mapper

        self.resolution = self.product_id.split("_")[2][-1]

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
        return [self.file_mapper(x) for x in self.file_hrefs["measurement"]]

    @property
    def metadata_dict(self) -> Dict[str, Any]:

        resolutions = {"F": "full", "H": "high", "M": "medium"}

        tmp = self._root.find(".//s1sarl1:sliceNumber")
        slice_number = tmp.text if tmp is not None else None
        tmp = self._root.find(".//s1sarl1:totalSlices")
        total_slices = tmp.text if tmp is not None else None

        result = {
            "start_datetime":
            str(self.start_datetime),
            "end_datetime":
            str(self.end_datetime),
            "s1:instrument_configuration_ID":
            self._root.findall(".//s1sarl1:instrumentConfigurationID")[0].text,
            "s1:datatake_id":
            self._root.findall(".//s1sarl1:missionDataTakeID")[0].text,
            "s1:product_timeliness":
            self._root.findall(".//s1sarl1:productTimelinessCategory")[0].text,
            "s1:processing_level":
            self.product_id.split("_")[3][0],
            "s1:resolution":
            resolutions[self.resolution],
            "s1:orbit_source":
            self.orbit_source(),
            "s1:slice_number":
            slice_number,
            "s1:total_slices":
            total_slices
        }

        return {k: v for k, v in result.items() if v is not None}

    def orbit_source(self) -> str:
        for resource in self._root.findall(
                ".//{http://www.esa.int/safe/sentinel-1.0}resource[@role]"):

            name = resource.find_attr("name", ".")
            if name is None or not name.endswith(".EOF"):
                continue

            role = resource.find_attr("role", ".")
            if role is None or not role.startswith("AUX_"):
                continue

            if role == "AUX_POE":
                return "POEORB"
            elif role == "AUX_RES":
                return "RESORB"
            elif role == "AUX_PRE":
                return "PREORB"
            else:
                raise RuntimeError(f"Invalid orbit file role found: {role}")

        return "DOWNLINK"
