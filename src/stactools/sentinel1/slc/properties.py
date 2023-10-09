from typing import Dict, TypeVar

import pystac
from pystac.extensions.sar import (
    FrequencyBand,
    ObservationDirection,
    Polarization,
    SarExtension,
)
from pystac.extensions.sat import OrbitState, SatExtension
from pystac.utils import str_to_datetime
from stactools.core.io.xml import XmlElement

T = TypeVar("T", pystac.Item, pystac.Asset)


class ProductDataEntry:
    def __init__(
        self,
        resolution_rng: float,
        resolution_azi: float,
        pixel_spacing_rng: float,
        pixel_spacing_azi: float,
        no_looks_rng: int,
        no_looks_azi: int,
        enl: float,
    ):
        self.resolution_rng = resolution_rng
        self.resolution_azi = resolution_azi
        self.pixel_spacing_rng = pixel_spacing_rng
        self.pixel_spacing_azi = pixel_spacing_azi
        self.no_looks_rng = no_looks_rng
        self.no_looks_azi = no_looks_azi
        self.enl = enl


product_data_summary: Dict[str, Dict[str, ProductDataEntry]] = {
    # https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-1-sar/products-algorithms/level-1/single-look-complex/stripmap
    "SM": {
        "S1": ProductDataEntry(1.7, 4.9, 1.5, 3.6, 1, 1, 1),
        "S2": ProductDataEntry(2.0, 4.9, 1.8, 4.2, 1, 1, 1),
        "S3": ProductDataEntry(2.5, 4.9, 2.2, 3.5, 1, 1, 1),
        "S4": ProductDataEntry(3.3, 4.9, 2.6, 4.1, 1, 1, 1),
        "S5": ProductDataEntry(3.3, 3.9, 2.9, 3.6, 1, 1, 1),
        "S6": ProductDataEntry(3.6, 4.9, 3.1, 4.1, 1, 1, 1),
    },
    # https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-1-sar/products-algorithms/level-1/single-look-complex/interferometric-wide-swath
    "IW": {
        "IW1": ProductDataEntry(2.7, 22.5, 2.3, 14.1, 1, 1, 1),
        "IW2": ProductDataEntry(3.1, 22.7, 2.3, 14.1, 1, 1, 1),
        "IW3": ProductDataEntry(3.5, 22.6, 2.3, 14.1, 1, 1, 1),
    },
    # https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-1-sar/products-algorithms/level-1/single-look-complex/extra-wide-swath
    "EW": {
        "EW1": ProductDataEntry(7.9, 43.7, 5.9, 19.9, 1, 1, 1),
        "EW2": ProductDataEntry(9.9, 44.3, 5.9, 19.9, 1, 1, 1),
        "EW3": ProductDataEntry(11.6, 45.2, 5.9, 19.9, 1, 1, 1),
        "EW4": ProductDataEntry(13.3, 45.6, 5.9, 19.9, 1, 1, 1),
        "EW5": ProductDataEntry(14.4, 44.0, 5.9, 19.9, 1, 1, 1),
    },
    # https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-1-sar/products-algorithms/level-1/single-look-complex/wave
    "WV": {
        "WV1": ProductDataEntry(2, 4.8, 1.8, 4.1, 1, 1, 1),
        "WV2": ProductDataEntry(3.1, 4.8, 2.7, 4.1, 1, 1, 1),
    },
}


def fill_common_sar_properties(sar_ext: SarExtension[T], manifest: XmlElement) -> None:
    """Fills the properties for SAR.

    Based on the sar Extension.py

    Args:
        sar_ext (SarExtension): The extension to be populated.
        manifest (XmlElement): manifest.safe file parsed into an XmlElement
    """
    # Fixed properties
    sar_ext.frequency_band = FrequencyBand("C")
    sar_ext.center_frequency = 5.405
    sar_ext.observation_direction = ObservationDirection.RIGHT

    # Read properties
    instrument_mode = manifest.find_text(".//s1sarl1:mode")
    if instrument_mode:
        sar_ext.instrument_mode = instrument_mode
    sar_ext.polarizations = [
        Polarization(x.text)
        for x in manifest.findall(".//s1sarl1:transmitterReceiverPolarisation")
    ]
    product_type = manifest.find_text(".//s1sarl1:productType")
    if product_type:
        sar_ext.product_type = product_type


def fill_swath_sar_properties(
    sar_ext: SarExtension[pystac.Asset], swath: str, polarisation: str
) -> None:
    """Fills the properties for SAR.

    Based on the sar Extension.py

    Args:
        sar_ext (SarExtension): The extension to be populated.
        swath (str): the swath ID for this particular asset
        polarisation (str): the polarisation for this particular asset
    """
    # Properties depending on mode and swath
    product_data = product_data_summary[sar_ext.instrument_mode][swath]

    sar_ext.polarizations = [Polarization(polarisation)]
    sar_ext.resolution_range = product_data.resolution_rng
    sar_ext.resolution_azimuth = product_data.resolution_azi
    sar_ext.pixel_spacing_range = product_data.pixel_spacing_rng
    sar_ext.pixel_spacing_azimuth = product_data.pixel_spacing_azi
    sar_ext.looks_range = product_data.no_looks_rng
    sar_ext.looks_azimuth = product_data.no_looks_azi
    sar_ext.looks_equivalent_number = product_data.enl


def fill_sat_properties(sat_ext: SatExtension[T], manifest: XmlElement) -> None:
    """Fills the properties for SAT.

    Based on the sat Extension.py

    Args:
        sat_ext (SatExtension): The extension to be populated.
        manifest (XmlElement): manifest.safe file parsed into an XmlElement
    """

    sat_ext.platform_international_designator = manifest.find_text(
        ".//safe:nssdcIdentifier"
    )

    orbit_state = manifest.find_text(".//s1:pass")
    if orbit_state:
        sat_ext.orbit_state = OrbitState(orbit_state.lower())

    orbit_number = manifest.find_text(".//safe:orbitNumber")
    if orbit_number:
        sat_ext.absolute_orbit = int(orbit_number)

    relative_orbit = manifest.find_text(".//safe:relativeOrbitNumber")
    if relative_orbit:
        sat_ext.relative_orbit = int(relative_orbit)

    ascending_node_time = manifest.find_text(".//s1:ascendingNodeTime")
    if ascending_node_time:
        sat_ext.anx_datetime = str_to_datetime(ascending_node_time)


def fill_processing_properties(item: pystac.Item, manifest: XmlElement) -> None:
    """Fills the properties for processing.

    Args:
        item (pystac.Item): The extension to be populated.
        manifest (XmlElement): manifest.safe file parsed into an XmlElement
    """
    schema_uri = "https://stac-extensions.github.io/processing/v1.1.0/schema.json"
    if item.stac_extensions is None:
        item.stac_extensions = [schema_uri]
    elif schema_uri not in item.stac_extensions:
        item.stac_extensions.append(schema_uri)

    facility_name = manifest.find_attr("name", ".//safe:facility/")
    if facility_name:
        item.properties["processing:facility"] = facility_name

    # SLCs are Level-1 products
    item.properties["processing:level"] = "L1"

    software = manifest.find(".//safe:software")
    if software is not None:
        name = software.get_attr("name")
        if name:
            item.properties["processing:software"] = {
                name: software.get_attr("version")
            }
