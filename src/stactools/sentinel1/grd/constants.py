import pystac
from pystac import ProviderRole
from pystac.link import Link
from pystac.extensions.eo import Band

INSPIRE_METADATA_ASSET_KEY = "inspire-metadata"
SAFE_MANIFEST_ASSET_KEY = "safe-manifest"
PRODUCT_METADATA_ASSET_KEY = "product-metadata"

SENTINEL_LICENSE = Link(
    rel="license",
    target="https://sentinel.esa.int/documents/" +
    "247904/690755/Sentinel_Data_Legal_Notice",
)

ACQUISITION_MODES = [
    "Stripmap (SM)",
    "Interferometric Wide Swath (IW)",
    "Extra Wide Swath (EW)",
    "Wave (WV)",
]
SENTINEL_CONSTELLATION = "Sentinel 1"

SENTINEL_PROVIDER = pystac.Provider(
    name="ESA",
    roles=[
        ProviderRole.PRODUCER,
        ProviderRole.PROCESSOR,
        ProviderRole.LICENSOR,
    ],
    url="https://earth.esa.int/web/guest/home",
)

SAFE_MANIFEST_ASSET_KEY = "safe-manifest"

SENTINEL_POLARISATIONS = {
    "vh":
    Band.create(
        name="VH",
        description="vertical transmit and horizontal receive",
    ),
    "hh":
    Band.create(
        name="HH",
        description="horizontal transmit and horizontal receive",
    ),
    "hv":
    Band.create(
        name="HV",
        description="horizontal transmit and vertical receive",
    ),
    "vv":
    Band.create(
        name="VV",
        description="vertical transmit and vertical receive",
    ),
}

SENTINEL_LICENSE = Link(
    rel="license",
    target="https://sentinel.esa.int/documents/" +
    "247904/690755/Sentinel_Data_Legal_Notice",
)
