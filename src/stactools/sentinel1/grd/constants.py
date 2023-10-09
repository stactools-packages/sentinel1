from datetime import datetime
from typing import Any, Dict

import pystac
from pystac import Extent, ProviderRole, SpatialExtent, TemporalExtent
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
    "SENTINEL_GRD_DESCRIPTION",
    "SENTINEL_GRD_START",
    "SENTINEL_GRD_EXTENT",
    "SENTINEL_GRD_PROVIDER",
    "SENTINEL_GRD_TECHNICAL_GUIDE",
    "SENTINEL_GRD_LICENSE",
    "SENTINEL_GRD_KEYWORDS",
    "SENTINEL_GRD_SAT",
    "SENTINEL_GRD_SAR",
    "SENTINEL_GRD_ASSETS",
]


SENTINEL_GRD_DESCRIPTION = (
    "Level-1 Ground Range Detected (GRD) products consist of focused SAR data that has been detected, multi-looked and projected to ground range using an Earth ellipsoid model. The ellipsoid projection of the GRD products is corrected using the terrain height specified in the product general annotation. "  # noqa: E501
    "The terrain height used varies in azimuth but is constant in range. Ground range coordinates are the slant range coordinates projected onto the ellipsoid of the Earth. Pixel values represent detected magnitude. Phase information is lost. The resulting product has approximately square spatial resolution "  # noqa: E501
    "and square pixel spacing with reduced speckle due to the multi-look processing. The noise vector annotation data set, within the product annotations, contains thermal noise vectors so that users can apply a thermal noise correction by subtracting the noise from the power detected image. "  # noqa: E501
    "The thermal noise correction is, for example, supported by the Sentinel-1 Toolbox (S1TBX). For the IW and EW GRD products, multi-looking is performed on each burst individually. All bursts in all sub-swaths are then seamlessly merged to form a single, contiguous, ground range detected image per polarization channel."  # noqa: E501
    "GRD products are available in three resolutions, characterised by the acquisition mode and the level of multi-looking applied: Full Resolution (FR), High Resolution (HR), Medium Resolution (MR)."  # noqa: E501
)

SENTINEL_GRD_START: datetime = str_to_datetime("2014-10-10T00:00:00Z")
SENTINEL_GRD_EXTENT = Extent(
    SpatialExtent([-180.0, -90.0, 180.0, 90.0]),
    TemporalExtent([[SENTINEL_GRD_START, None]]),
)

SENTINEL_GRD_PROVIDER = pystac.Provider(
    name="Sinergise",
    roles=[
        ProviderRole.HOST,
        ProviderRole.PROCESSOR,
        ProviderRole.LICENSOR,
    ],
    url="https://registry.opendata.aws/sentinel-1/",
)

SENTINEL_GRD_TECHNICAL_GUIDE = Link(
    title="Sentinel-1 Ground Range Detected (GRD) Technical Guide",
    rel="about",
    target="https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-1-sar/products-algorithms/level-1-algorithms/ground-range-detected",  # noqa: E501
)

SENTINEL_GRD_LICENSE = Link(
    title="Sentinel License",
    rel="license",
    target="https://scihub.copernicus.eu/twiki/do/view/SciHubWebPortal/TermsConditions",
)

SENTINEL_GRD_KEYWORDS = ["ground", "sentinel", "copernicus", "esa", "sar"]

SENTINEL_GRD_SAT = {
    "orbit_state": [sat.OrbitState.ASCENDING, sat.OrbitState.DESCENDING]
}

SENTINEL_GRD_SAR: Dict[str, Any] = {
    "looks_range": [2, 3, 5, 6],
    "product_type": ["GRD"],
    "looks_azimuth": [1, 2, 6],
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
    "instrument_mode": ["IW", "EW", "SM"],
    "center_frequency": [5.405],
    "resolution_range": [9, 20, 23, 50, 93],
    "resolution_azimuth": [9, 22, 23, 50, 87],
    "pixel_spacing_range": [3.5, 10, 25, 40],
    "observation_direction": [sar.ObservationDirection.RIGHT],
    "pixel_spacing_azimuth": [3.5, 10, 25, 40],
    "looks_equivalent_number": [3.7, 29.7, 398.4, 4.4, 81.8, 2.8, 10.7, 123.7],
}

SENTINEL_GRD_ASSETS = {
    "vh": AssetDefinition(
        {
            "title": "VH Data",
            "type": pystac.MediaType.COG,
            "description": "VH polarization backscattering coefficient, 16-bit DN.",
            "roles": ["data"],
        }
    ),
    "hh": AssetDefinition(
        {
            "title": "HH Data",
            "type": pystac.MediaType.COG,
            "description": "HH polarization backscattering coefficient, 16-bit DN.",
            "roles": ["data"],
        }
    ),
    "hv": AssetDefinition(
        {
            "title": "HV Data",
            "type": pystac.MediaType.COG,
            "description": "HV polarization backscattering coefficient, 16-bit DN.",
            "roles": ["data"],
        }
    ),
    "vv": AssetDefinition(
        {
            "title": "VV Data",
            "type": pystac.MediaType.COG,
            "description": "VV polarization backscattering coefficient, 16-bit DN.",
            "roles": ["data"],
        }
    ),
    "schema-calibration-hh": AssetDefinition(
        {
            "title": "HH Calibration Schema",
            "type": pystac.MediaType.XML,
            "description": (
                "Calibration metadata including calibration information and the beta nought, "
                "sigma nought, gamma and digital number look-up tables that can be used for "
                "absolute product calibration."
            ),
            "roles": ["metadata"],
        }
    ),
    "schema-calibration-hv": AssetDefinition(
        {
            "title": "HV Calibration Schema",
            "type": pystac.MediaType.XML,
            "description": (
                "Calibration metadata including calibration information and the beta nought, "
                "sigma nought, gamma and digital number look-up tables that can be used for "
                "absolute product calibration."
            ),
            "roles": ["metadata"],
        }
    ),
    "schema-calibration-vh": AssetDefinition(
        {
            "title": "VH Calibration Schema",
            "type": pystac.MediaType.XML,
            "description": (
                "Calibration metadata including calibration information and the beta nought, "
                "sigma nought, gamma and digital number look-up tables that can be used for "
                "absolute product calibration."
            ),
            "roles": ["metadata"],
        }
    ),
    "schema-calibration-vv": AssetDefinition(
        {
            "title": "VV Calibration Schema",
            "type": pystac.MediaType.XML,
            "description": (
                "Calibration metadata including calibration information and the beta nought, "
                "sigma nought, gamma and digital number look-up tables that can be used for "
                "absolute product calibration."
            ),
            "roles": ["metadata"],
        }
    ),
    "schema-noise-hh": AssetDefinition(
        {
            "title": "HH Noise Schema",
            "type": pystac.MediaType.XML,
            "description": "Estimated thermal noise look-up tables",
            "roles": ["metadata"],
        }
    ),
    "schema-noise-hv": AssetDefinition(
        {
            "title": "HV Noise Schema",
            "type": pystac.MediaType.XML,
            "description": "Estimated thermal noise look-up tables",
            "roles": ["metadata"],
        }
    ),
    "schema-noise-vh": AssetDefinition(
        {
            "title": "VH Noise Schema",
            "type": pystac.MediaType.XML,
            "description": "Estimated thermal noise look-up tables",
            "roles": ["metadata"],
        }
    ),
    "schema-noise-vv": AssetDefinition(
        {
            "title": "VV Noise Schema",
            "type": pystac.MediaType.XML,
            "description": "Estimated thermal noise look-up tables",
            "roles": ["metadata"],
        }
    ),
    "schema-product-hh": AssetDefinition(
        {
            "title": "HH Product Schema",
            "type": pystac.MediaType.XML,
            "description": (
                "Describes the main characteristics corresponding to the band: state of the "
                "platform during acquisition, image properties, Doppler information, geographic "
                "location, etc."
            ),
            "roles": ["metadata"],
        }
    ),
    "schema-product-hv": AssetDefinition(
        {
            "title": "HV Product Schema",
            "type": pystac.MediaType.XML,
            "description": (
                "Describes the main characteristics corresponding to the band: state of the "
                "platform during acquisition, image properties, Doppler information, geographic "
                "location, etc."
            ),
            "roles": ["metadata"],
        }
    ),
    "schema-product-vh": AssetDefinition(
        {
            "title": "VH Product Schema",
            "type": pystac.MediaType.XML,
            "description": (
                "Describes the main characteristics corresponding to the band: state of the "
                "platform during acquisition, image properties, Doppler information, geographic "
                "location, etc."
            ),
            "roles": ["metadata"],
        }
    ),
    "schema-product-vv": AssetDefinition(
        {
            "title": "VV Product Schema",
            "type": pystac.MediaType.XML,
            "description": (
                "Describes the main characteristics corresponding to the band: state of the "
                "platform during acquisition, image properties, Doppler information, geographic "
                "location, etc."
            ),
            "roles": ["metadata"],
        }
    ),
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
