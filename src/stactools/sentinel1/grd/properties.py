from stactools.core.io.xml import XmlElement
from pystac.extensions.sar import FrequencyBand, Polarization
from pystac.extensions.sat import OrbitState


def fill_sar_properties(sar_ext, href):
    """Fills the properties for SAR.

    Based on the sar Extension.py

    Args:
        input_ext (pystac.extensions.sar.SarExtension): The extension to be populated.
        href (str): The HREF to the scene, this is expected to be an XML file.

    Returns:
        pystac.Asset: An asset with the SAR relevant properties.
    """
    # Read meta file
    root = XmlElement.from_file(href)

    # Fixed properties
    sar_ext.frequency_band = FrequencyBand("C")
    sar_ext.center_frequency = 5.405
    sar_ext.looks_range = 5
    sar_ext.looks_azimuth = 1
    sar_ext.pixel_spacing_range = 10

    # Read properties
    sar_ext.instrument_mode = root.findall(".//s1sarl1:mode")[0].text
    sar_ext.polarizations = [
        Polarization(x.text)
        for x in root.findall(".//s1sarl1:transmitterReceiverPolarisation")
    ]
    sar_ext.product_type = root.findall(".//s1sarl1:productType")[0].text


def fill_sat_properties(sat_ext, href):
    """Fills the properties for SAR.

    Based on the sar Extension.py

    Args:
        input_ext (pystac.extensions.sar.SarExtension): The extension to be populated.
        href (str): The HREF to the scene, this is expected to be an XML file.

    Returns:
        pystac.Asset: An asset with the SAR relevant properties.
    """
    # Read meta file
    root = XmlElement.from_file(href)

    sat_ext.platform_international_designator = root.findall(
        ".//safe:nssdcIdentifier")[0].text

    orbit_state = root.findall(".//s1:pass")[0].text
    sat_ext.orbit_state = OrbitState(orbit_state.lower())

    sat_ext.absolute_orbit = int(root.findall(".//safe:orbitNumber")[0].text)

    sat_ext.relative_orbit = int(
        root.findall(".//safe:relativeOrbitNumber")[0].text)


def fill_proj_properties(proj_ext, meta_links, product_meta):
    """Fills the properties for SAR.

    Based on the sar Extension.py

    Args:
        input_ext (pystac.extensions.sar.SarExtension): The extension to be populated.
        href (str): The HREF to the scene, this is expected to be an XML file.

    Returns:
        pystac.Asset: An asset with the SAR relevant properties.
    """
    # Read meta file
    links = meta_links.create_product_asset()
    root = XmlElement.from_file(links[0][1].href)

    proj_ext.epsg = 4326

    proj_ext.geometry = product_meta.geometry

    proj_ext.bbox = product_meta.bbox

    x_size = int(root.findall(".//numberOfSamples")[0].text)
    y_size = int(root.findall(".//numberOfLines")[0].text)

    proj_ext.shape = [x_size, y_size]
