from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from pystac.utils import str_to_datetime
from shapely.geometry import Polygon, mapping
from stactools.core.io import ReadHrefModifier
from stactools.core.io.xml import XmlElement

from .metadata_links import MetadataLinks


class ProductMetadataError(Exception):
    pass


def get_shape(
    meta_links: MetadataLinks,
    read_href_modifier: Optional[ReadHrefModifier],
    **kwargs: Any,
) -> List[int]:
    links = meta_links.create_product_asset()
    root = XmlElement.from_file(links[0][1].href, read_href_modifier, **kwargs)

    num_samples = root.find_text(".//numberOfSamples")
    num_lines = root.find_text(".//numberOfLines")

    if num_samples and num_lines:
        x_size = int(num_samples)
        y_size = int(num_lines)
        return [x_size, y_size]

    raise ValueError(
        "Cannot determine shape, samples and lines, using product metadata "
        f"in {links[0][1].href}"
    )


class ProductMetadata:
    def __init__(
        self,
        href: str,
        file_hrefs: Dict[str, List[str]],
        file_mapper: Callable[[str], str],
        manifest: XmlElement,
    ) -> None:
        self.href = href
        self._root = manifest
        self.file_hrefs = file_hrefs
        self.file_mapper = file_mapper

        def _get_geometries() -> Tuple[List[float], Dict[str, Any]]:
            # Find the footprint descriptor
            footprint_text = self._root.find_text(".//gml:coordinates")
            if footprint_text is None:
                raise ProductMetadataError(
                    f"Cannot parse footprint from product metadata at {self.href}"
                )

            # Convert to values
            footprint_value = [
                float(x) for x in footprint_text.replace(" ", ",").split(",")
            ]

            footprint_points = [
                p[::-1] for p in list(zip(*[iter(footprint_value)] * 2))
            ]

            footprint_polygon = Polygon(footprint_points)
            geometry = mapping(footprint_polygon)
            bbox = list(footprint_polygon.bounds)

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
                "Cannot determine product ID using product metadata " f"at {self.href}"
            )
        else:
            return result

    @property
    def get_datetime(self) -> datetime:
        start_time = self._root.find_text(".//safe:startTime")
        end_time = self._root.find_text(".//safe:stopTime")

        if start_time is not None:
            central_time = (
                datetime.strptime(str(start_time), "%Y-%m-%dT%H:%M:%S.%f")
                + (
                    datetime.strptime(str(end_time), "%Y-%m-%dT%H:%M:%S.%f")
                    - datetime.strptime(str(start_time), "%Y-%m-%dT%H:%M:%S.%f")
                )
                / 2
            )

        if central_time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.href}"
            )
        else:
            return str_to_datetime(str(central_time))

    @property
    def start_datetime(self) -> datetime:
        time = self._root.find_text(".//safe:startTime")

        if time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.href}"
            )
        else:
            return str_to_datetime(f"{time}Z")

    @property
    def end_datetime(self) -> datetime:
        time = self._root.findall(".//safe:stopTime")

        if time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.href}"
            )
        else:
            return str_to_datetime(f"{time[0].text}Z")

    @property
    def platform(self) -> Optional[str]:

        family_name = self._root.findall(".//safe:familyName")[0].text
        assert family_name is not None
        platform_name = self._root.findall(".//safe:number")[0].text
        assert platform_name is not None

        return f"{family_name}{platform_name}"

    @property
    def cycle_number(self) -> Optional[str]:

        return self._root.findall(".//safe:cycleNumber")[0].text

    @property
    def image_paths(self) -> List[str]:
        return [self.file_mapper(x) for x in self.file_hrefs["measurement"]]

    def orbit_source(self) -> str:
        for resource in self._root.findall(
            ".//{http://www.esa.int/safe/sentinel-1.0}resource[@role]"
        ):

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
