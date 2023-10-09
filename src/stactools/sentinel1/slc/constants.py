from datetime import datetime
from itertools import product
from typing import Any, Dict

import pystac
from pystac import Extent, SpatialExtent, TemporalExtent
from pystac.extensions import sar, sat
from pystac.extensions.item_assets import AssetDefinition
from pystac.link import Link
from pystac.utils import str_to_datetime

from ..constants import (
    ACQUISITION_MODES,
    INSPIRE_METADATA_ASSET_KEY,
    PRODUCT_METADATA_ASSET_KEY,
    SAFE_MANIFEST_ASSET_KEY,
    SENTINEL_CONSTELLATION,
    SENTINEL_LICENSE,
    SENTINEL_PLATFORMS,
    SENTINEL_POLARIZATIONS,
    SENTINEL_PROVIDER,
)

__all__ = [
    "INSPIRE_METADATA_ASSET_KEY",
    "SAFE_MANIFEST_ASSET_KEY",
    "PRODUCT_METADATA_ASSET_KEY",
    "SENTINEL_LICENSE",
    "SENTINEL_PLATFORMS",
    "ACQUISITION_MODES",
    "SENTINEL_CONSTELLATION",
    "SENTINEL_PROVIDER",
    "SENTINEL_POLARIZATIONS",
    "SENTINEL_SLC_DESCRIPTION",
    "SENTINEL_SLC_START",
    "SENTINEL_SLC_EXTENT",
    "SENTINEL_SLC_TECHNICAL_GUIDE",
    "SENTINEL_SLC_LICENSE",
    "SENTINEL_SLC_KEYWORDS",
    "SENTINEL_SLC_SAT",
    "SENTINEL_SLC_SAR",
    "SENTINEL_SLC_SWATHS",
    "SENTINEL_SLC_ASSETS",
    "SENTINEL_SLC_IW_TPRE",
    "SENTINEL_SLC_IW_TBEAM",
    "SENTINEL_SLC_IW_TORB",
    "SENTINEL_SLC_EW_TPRE",
    "SENTINEL_SLC_EW_TBEAM",
    "SENTINEL_SLC_EW_TORB",
]

SENTINEL_SLC_DESCRIPTION = (
    "Level-1 Single Look Complex (SLC) products are images in the slant range by azimuth imaging plane, in the image plane of satellite data acquisition. Each image pixel is represented by a complex (I and Q) magnitude value and therefore contains both amplitude and phase information. Each I and Q value "  # noqa: E501
    "is 16 bits per pixel. The processing for all SLC products results in a single look in each dimension using the full available signal bandwidth. The imagery is geo-referenced using orbit and attitude data from the satellite. SLC images are produced in a zero Doppler geometry. This convention is common "  # noqa: E501
    "with the standard slant range products available from other SAR sensors."
)

SENTINEL_SLC_START: datetime = str_to_datetime("2014-10-10T00:00:00Z")
SENTINEL_SLC_EXTENT = Extent(
    SpatialExtent([-180.0, -90.0, 180.0, 90.0]),
    TemporalExtent([[SENTINEL_SLC_START, None]]),
)

SENTINEL_SLC_TECHNICAL_GUIDE = Link(
    title="Sentinel-1 Single Look Complex (SLC) Technical Guide",
    rel="about",
    target="https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-1-sar/products-algorithms/level-1-algorithms/single-look-complex",  # noqa: E501
)

SENTINEL_SLC_LICENSE = Link(
    title="Sentinel License",
    rel="license",
    target="https://scihub.copernicus.eu/twiki/do/view/SciHubWebPortal/TermsConditions",
)

SENTINEL_SLC_KEYWORDS = ["ground", "sentinel", "copernicus", "esa", "sar"]

SENTINEL_SLC_SAT = {
    "orbit_state": [sat.OrbitState.ASCENDING, sat.OrbitState.DESCENDING]
}

SENTINEL_SLC_SAR: Dict[str, Any] = {
    "looks_range": [1],
    "product_type": ["SLC"],
    "looks_azimuth": [1],
    "polarizations": [
        sar.Polarization.HH,
        sar.Polarization.VV,
        sar.Polarization.HV,
        sar.Polarization.VH,
        [
            sar.Polarization.HH,
            sar.Polarization.HV,
        ],
        [
            sar.Polarization.VV,
            sar.Polarization.VH,
        ],
    ],
    "frequency_band": [sar.FrequencyBand.C],
    "instrument_mode": ["IW", "EW", "SM", "WV"],
    "center_frequency": [5.405],
    "resolution_range": [
        1.7,
        2.0,
        2.5,
        2.7,
        3.1,
        3.3,
        3.6,
        3.5,
        7.9,
        9.9,
        11.6,
        13.3,
        14.4,
    ],
    "resolution_azimuth": [
        3.9,
        4.9,
        22.5,
        22.6,
        22.7,
        43.7,
        44.3,
        45.2,
        45.6,
        44.0,
    ],
    "pixel_spacing_range": [
        1.5,
        1.8,
        2.2,
        2.3,
        2.6,
        2.9,
        3.1,
        5.9,
    ],
    "pixel_spacing_azimuth": [
        3.5,
        3.6,
        4.1,
        4.2,
        14.1,
        19.9,
    ],
    "observation_direction": [sar.ObservationDirection.RIGHT],
    "looks_equivalent_number": [1],
}


SENTINEL_SLC_SWATHS = [
    "IW1",
    "IW2",
    "IW3",
    "EW1",
    "EW2",
    "EW3",
    "EW4",
    "EW5",
    "S1",
    "S2",
    "S3",
    "S4",
    "S5",
    "S6",
    "WV1",
    "WV2",
]


SENTINEL_SLC_IMAGE_ASSET_DEFINITIONS = {
    f"{swath.lower()}-{pol.lower()}": AssetDefinition(
        {
            "title": f"{swath.upper()} {pol.upper()} Data",
            "type": pystac.MediaType.COG,
            "description": (
                f"{swath.upper()} {pol.upper()} polarization backscattering"
                "coefficient, 16-bit DN."
            ),
            "roles": ["data"],
        }
    )
    for swath, pol in product(SENTINEL_SLC_SWATHS, SENTINEL_POLARIZATIONS.keys())
}

SENTINEL_SLC_SCHEMA_CALIBRATION_ASSET_DEFINITIONS = {
    f"schema-calibration-{swath.lower()}-{pol.lower()}": AssetDefinition(
        {
            "title": f"{pol.upper()} Calibration Schema",
            "type": pystac.MediaType.XML,
            "description": (
                "Calibration metadata including calibration information and the beta nought, "
                "sigma nought, gamma and digital number look-up tables that can be used for "
                "absolute product calibration."
            ),
            "roles": ["metadata"],
        }
    )
    for swath, pol in product(SENTINEL_SLC_SWATHS, SENTINEL_POLARIZATIONS.keys())
}

SENTINEL_SLC_SCHEMA_NOISE_ASSET_DEFINITIONS = {
    f"schema-noise-{swath.lower()}-{pol.lower()}": AssetDefinition(
        {
            "title": f"{pol.upper()} Noise Schema",
            "type": pystac.MediaType.XML,
            "description": "Estimated thermal noise look-up tables",
            "roles": ["metadata"],
        }
    )
    for swath, pol in product(SENTINEL_SLC_SWATHS, SENTINEL_POLARIZATIONS.keys())
}

SENTINEL_SLC_SCHEMA_PRODUCT_ASSET_DEFINITIONS = {
    f"schema-product-{swath.lower()}-{pol.lower()}": AssetDefinition(
        {
            "title": f"{pol.upper()} Product Schema",
            "type": pystac.MediaType.XML,
            "description": (
                "Describes the main characteristics corresponding to the band: state of the "
                "platform during acquisition, image properties, Doppler information, geographic "
                "location, etc."
            ),
            "roles": ["metadata"],
        }
    )
    for swath, pol in product(SENTINEL_SLC_SWATHS, SENTINEL_POLARIZATIONS.keys())
}

SENTINEL_SLC_ASSETS = {
    **SENTINEL_SLC_IMAGE_ASSET_DEFINITIONS,
    **SENTINEL_SLC_SCHEMA_CALIBRATION_ASSET_DEFINITIONS,
    **SENTINEL_SLC_SCHEMA_NOISE_ASSET_DEFINITIONS,
    **SENTINEL_SLC_SCHEMA_PRODUCT_ASSET_DEFINITIONS,
    "safe-manifest": AssetDefinition(
        {
            "title": "Manifest File",
            "type": pystac.MediaType.XML,
            "description": (
                "General product metadata in XML format. Contains a high-level textual "
                "description of the product and references to all of product's components, "
                "the product metadata, including the product identification and the resource "
                "references, and references to the physical location of each component file "
                "contained in the product."
            ),
            "roles": ["metadata"],
        }
    ),
    "thumbnail": AssetDefinition(
        {
            "title": "Preview Image",
            "type": pystac.MediaType.PNG,
            "description": (
                "An averaged, decimated preview image in PNG format. Single polarization "
                "products are represented with a grey scale image. Dual polarization products "
                "are represented by a single composite colour image in RGB with the red channel "
                "(R) representing the  co-polarization VV or HH), the green channel (G) "
                "represents the cross-polarization (VH or HV) and the blue channel (B) "
                "represents the ratio of the cross an co-polarizations."
            ),
            "roles": ["thumbnail"],
        }
    ),
}


SENTINEL_SLC_IW_TPRE = 2.299849  # Preamble length
SENTINEL_SLC_IW_TBEAM = 2.758273  # Beam cycle time
SENTINEL_SLC_IW_TORB = 12 * 86400 / 175  # Nominal orbit duration

SENTINEL_SLC_EW_TPRE = 2.299970  # Preamble length
SENTINEL_SLC_EW_TBEAM = 3.038376  # Beam cycle time
SENTINEL_SLC_EW_TORB = 12 * 86400 / 175  # Nominal orbit duration
