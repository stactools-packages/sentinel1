from datetime import datetime
from typing import Any, Dict

import pystac
from pystac import Extent, ProviderRole, SpatialExtent, TemporalExtent
from pystac.extensions import sar
from pystac.link import Link
from pystac.utils import str_to_datetime

# General Sentinel-1 Constants
# -
SENTINEL_LICENSE = Link(
    rel="license",
    target="https://sentinel.esa.int/documents/"
    + "247904/690755/Sentinel_Data_Legal_Notice",
)

SENTINEL_INSTRUMENTS = ["c-sar"]
SENTINEL_CONSTELLATION = "sentinel-1"
SENTINEL_PLATFORMS = ["sentinel-1a", "sentinel-1b"]
SENTINEL_FREQUENCY_BAND = sar.FrequencyBand.C
SENTINEL_CENTER_FREQUENCY = 5.405
SENTINEL_OBSERVATION_DIRECTION = sar.ObservationDirection.RIGHT

SENTINEL_PROVIDER = pystac.Provider(
    name="ESA",
    roles=[ProviderRole.LICENSOR, ProviderRole.PRODUCER],
    url="https://sentinel.esa.int/web/sentinel/missions/sentinel-1",
)

SENTINEL_LICENSE = Link(
    rel="license", target="https://spacedata.copernicus.eu/data-offer/legal-documents"
)

# RTC-specific constants
# -
SENTINEL_RTC_PROVIDER = pystac.Provider(
    name="Indigo Ag Inc.",
    roles=[ProviderRole.LICENSOR, ProviderRole.PROCESSOR, ProviderRole.HOST],
    url="https://registry.opendata.aws/sentinel-1-rtc-indigo",
    extra_fields={
        "processing:level": "L3",
        "processing:lineage": "https://sentinel-s1-rtc-indigo-docs.s3-us-west-2.amazonaws.com/methodology.html",  # noqa: E501
        "processing:software": {"S1TBX": "7.0.2"},
    },
)

SENTINEL_RTC_LICENSE = Link(
    rel="license", target="https://www.indigoag.com/forms/atlas-sentinel-license"
)

SENTINEL_RTC_DESCRIPTION = "Sentinel1 radiometric terrain corrected backscatter (RTC) over CONUS. The Sentinel-1 mission is a constellation of C-band Synthetic Aperture Radar (SAR) satellites from the European Space Agency launched since 2014. These satellites collect observations of radar backscatter intensity day or night, regardless of the weather conditions, making them enormously valuable for environmental monitoring. These radar data have been processed from original Ground Range Detected (GRD) scenes into a Radiometrically Terrain Corrected, tiled product suitable for analysis. This product is available over the Contiguous United States (CONUS) since 2017 when Sentinel-1 data became globally available."  # noqa: E501

SENTINEL_RTC_START: datetime = str_to_datetime("2016-07-29T00:00:00Z")
SENTINEL_RTC_EXTENT = Extent(
    SpatialExtent([-124.73460, 24.54254, -66.89191, 49.36949]),
    TemporalExtent([[SENTINEL_RTC_START, None]]),
)

utm_zones = ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19"]
SENTINEL_RTC_EPSGS = [int(f"326{x}") for x in utm_zones]

# RTC is derived from S1 GRD, so include input GRD properties for IW2 (center swath)
# https://sentinel.esa.int/web/sentinel/technical-guides/sentinel-1-sar/products-algorithms/level-1-algorithms/ground-range-detected/iw
SENTINEL_RTC_SAR: Dict[str, Any] = {
    "instrument_mode": "IW",
    "product_type": "RTC",
    "polarizations": [sar.Polarization.VV, sar.Polarization.VH],
    "resolution_range": 20.3,
    "resolution_azimuth": 22.6,
    "pixel_spacing_range": 10,
    "pixel_spacing_azimuth": 10,
    "looks_equivalent_number": 4.3,
    "looks_range": 5,
    "looks_azimuth": 1,
    "gsd": 20,  # final MGRS pixel posting
}
