from typing import Dict, Optional

import pystac
from pystac.extensions.sar import (FrequencyBand, ObservationDirection,
                                   Polarization)
from pystac.extensions.sat import OrbitState
from stactools.core.io import ReadHrefModifier
from stactools.core.io.xml import XmlElement


class ProductDataEntry:
    def __init__(self, resolution_rng: float, resolution_azi: float,
                 pixel_spacing_rng: float, pixel_spacing_azi: float,
                 no_looks_rng: int, no_looks_azi: int, enl: float):
        self.resolution_rng = resolution_rng
        self.resolution_azi = resolution_azi
        self.pixel_spacing_rng = pixel_spacing_rng
        self.pixel_spacing_azi = pixel_spacing_azi
        self.no_looks_rng = no_looks_rng
        self.no_looks_azi = no_looks_azi
        self.enl = enl


# Sourced from Sentinel-1 Product Definition: Table 5-1
#   https://sentinel.esa.int/web/sentinel/user-guides/sentinel-1-sar/document-library/-/asset_publisher/1dO7RF5fJMbd/content/sentinel-1-product-definition
product_data_summary: Dict[str, Dict[str, ProductDataEntry]] = {
    "SM": {
        "F": ProductDataEntry(9, 9, 3.5, 3.5, 2, 2, 3.7),
        "H": ProductDataEntry(23, 23, 10, 10, 6, 6, 29.7),
        "M": ProductDataEntry(84, 84, 40, 40, 22, 22, 398.4)
    },
    "IW": {
        "H": ProductDataEntry(20, 22, 10, 10, 5, 1, 4.4),
        "M": ProductDataEntry(88, 87, 40, 40, 22, 5, 81.8)
    },
    "EW": {
        "H": ProductDataEntry(50, 50, 25, 25, 3, 1, 2.7),
        "M": ProductDataEntry(93, 87, 40, 40, 6, 2, 10.7)
    },
    "WV": {
        "M": ProductDataEntry(52, 51, 25, 25, 13, 13, 123.7)
    }
}


def fill_sar_properties(sar_ext: pystac.extensions.sar.SarExtension,
                        href: str,
                        resolution: str,
                        read_href_modifier: Optional[ReadHrefModifier] = None):
    """Fills the properties for SAR.

    Based on the sar Extension.py

    Args:
        sar_ext (pystac.extensions.sar.SarExtension): The extension to be populated.
        href (str): The HREF to the scene, this is expected to be an XML file.
        resolution (str): product resolution, needed to select metadata from
            static values in product_data_summary
        read_href_modifier: A function that takes an HREF and returns a modified HREF.
            This can be used to modify a HREF to make it readable, e.g. appending
            an Azure SAS token or creating a signed URL.

    Returns:
        pystac.Asset: An asset with the SAR relevant properties.
    """
    # Read meta file
    root = XmlElement.from_file(href, read_href_modifier)

    # Fixed properties
    sar_ext.frequency_band = FrequencyBand("C")
    sar_ext.center_frequency = 5.405
    sar_ext.observation_direction = ObservationDirection.RIGHT

    # Read properties
    sar_ext.instrument_mode = root.findall(".//s1sarl1:mode")[0].text
    sar_ext.polarizations = [
        Polarization(x.text)
        for x in root.findall(".//s1sarl1:transmitterReceiverPolarisation")
    ]
    sar_ext.product_type = root.findall(".//s1sarl1:productType")[0].text

    # Properties depending on mode and resolution
    product_data = product_data_summary[sar_ext.instrument_mode][resolution]

    sar_ext.resolution_range = product_data.resolution_rng
    sar_ext.resolution_azimuth = product_data.resolution_azi
    sar_ext.pixel_spacing_range = product_data.pixel_spacing_rng
    sar_ext.pixel_spacing_azimuth = product_data.pixel_spacing_azi
    sar_ext.looks_range = product_data.no_looks_rng
    sar_ext.looks_azimuth = product_data.no_looks_azi
    sar_ext.looks_equivalent_number = product_data.enl


def fill_sat_properties(sat_ext,
                        href,
                        read_href_modifier: Optional[ReadHrefModifier] = None):
    """Fills the properties for SAR.

    Based on the sar Extension.py

    Args:
        sat_ext (pystac.extensions.sar.SarExtension): The extension to be populated.
        href (str): The HREF to the scene, this is expected to be an XML file.
        read_href_modifier: A function that takes an HREF and returns a modified HREF.
            This can be used to modify a HREF to make it readable, e.g. appending
            an Azure SAS token or creating a signed URL.

    Returns:
        pystac.Asset: An asset with the SAR relevant properties.
    """
    # Read meta file
    root = XmlElement.from_file(href, read_href_modifier)

    sat_ext.platform_international_designator = root.findall(
        ".//safe:nssdcIdentifier")[0].text

    orbit_state = root.findall(".//s1:pass")[0].text
    sat_ext.orbit_state = OrbitState(orbit_state.lower())

    sat_ext.absolute_orbit = int(root.findall(".//safe:orbitNumber")[0].text)

    sat_ext.relative_orbit = int(
        root.findall(".//safe:relativeOrbitNumber")[0].text)
