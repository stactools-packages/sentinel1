import os
from typing import List, Tuple

import pystac

from ..metadata_links import MetadataLinks, extract_properties


def get_swath_and_polarisation(href: str) -> Tuple[str, str]:
    swath, polarisation = extract_properties(href, ["swath", "polarisation"])
    return (swath.upper(), polarisation.upper())


class SLCMetadataLinks(MetadataLinks):
    @property
    def annotation_hrefs(self) -> List[Tuple[str, str]]:
        return [
            (
                "schema-product-{}-{}".format(*get_swath_and_polarisation(x)),
                os.path.join(self.granule_href, self.map_filename(x)),
            )
            for x in self.grouped_hrefs["annotation"]
            if x.endswith("xml")
        ]

    @property
    def calibration_hrefs(self) -> List[Tuple[str, str]]:
        return [
            (
                "schema-calibration-{}-{}".format(
                    *get_swath_and_polarisation(x)
                ),
                os.path.join(self.granule_href, self.map_filename(x)),
            )
            for x in self.grouped_hrefs["calibration_calibration"]
        ]

    @property
    def noise_hrefs(self) -> List[Tuple[str, str]]:
        return [
            (
                "schema-noise-{}-{}".format(*get_swath_and_polarisation(x)),
                os.path.join(self.granule_href, self.map_filename(x)),
            )
            for x in self.grouped_hrefs["calibration_noise"]
        ]

    def create_product_asset(self) -> List[Tuple[str, pystac.asset.Asset]]:
        assets = []
        desc = (
            "Describes the main characteristics corresponding to the band: state of the "
            "platform during acquisition, image properties, Doppler information, geographic "
            "location, etc."
        )
        for key, href in self.annotation_hrefs:
            # Extract polarisation from href
            swath, polarisation = get_swath_and_polarisation(href)
            if polarisation:
                # Add polarisation to title
                title = f"{polarisation} {swath} Product Schema"
                asset = pystac.Asset(
                    href=href,
                    media_type=pystac.MediaType.XML,
                    title=title,
                    roles=["metadata"],
                    description=desc,
                )
                assets.append((key, asset))
        return assets

    def create_calibration_asset(self) -> List[Tuple[str, pystac.asset.Asset]]:
        assets = []
        desc = (
            "Calibration metadata including calibration information and the beta nought, "
            "sigma nought, gamma and digital number look-up tables that can be used for "
            "absolute product calibration."
        )
        for key, href in self.calibration_hrefs:
            # Extract polarisation from href
            polarisation, swath = get_swath_and_polarisation(href)
            if polarisation:
                # Add polarisation to title
                title = f"{polarisation} {swath} Calibration Schema"
                asset = pystac.Asset(
                    href=href,
                    media_type=pystac.MediaType.XML,
                    title=title,
                    roles=["metadata"],
                    description=desc,
                )
                assets.append((key, asset))
        return assets

    def create_noise_asset(self) -> List[Tuple[str, pystac.asset.Asset]]:
        assets = []
        for key, href in self.noise_hrefs:
            # Extract polarisation from href
            polarisation, swath = get_swath_and_polarisation(href)
            if polarisation:
                # Add polarisation to title
                title = f"{polarisation} {swath} Noise Schema"
                asset = pystac.Asset(
                    href=href,
                    media_type=pystac.MediaType.XML,
                    title=title,
                    roles=["metadata"],
                    description="Estimated thermal noise look-up tables",
                )
                assets.append((key, asset))
        return assets
