import os
from typing import List, Optional

import pystac
from stactools.core.io.xml import XmlElement

from .constants import SAFE_MANIFEST_ASSET_KEY


class ManifestError(Exception):
    pass


class MetadataLinks:
    def __init__(
        self,
        granule_href: str,
    ):
        self.granule_href = granule_href
        self.href = os.path.join(granule_href, "manifest.safe")

        root = XmlElement.from_file(self.href)
        data_object_section = root.find("dataObjectSection")
        if data_object_section is None:
            raise ManifestError(
                f"Manifest at {self.href} does not have a dataObjectSection")

        self._data_object_section = data_object_section
        self.product_metadata_href = os.path.join(granule_href,
                                                  "manifest.safe")

    def _find_href(self, xpaths: List[str]) -> Optional[str]:
        file_path = None
        for xpath in xpaths:
            file_path = self._data_object_section.find_attr("href", xpath)
            if file_path is not None:
                break

        if file_path is None:
            return None
        else:
            # Remove relative prefix that some paths have
            file_path = file_path.strip("./")
            return os.path.join(self.granule_href, file_path)

    @property
    def thumbnail_href(self) -> Optional[str]:
        preview = os.path.join(self.granule_href, "preview")
        return os.path.join(preview, "quick-look.png")

    @property
    def annotation_hrefs(self) -> List[str]:
        annotation_path = os.path.join(self.granule_href, "annotation")
        return [
            os.path.join(annotation_path, x)
            for x in os.listdir(annotation_path) if x.endswith("xml")
        ]

    @property
    def calibration_hrefs(self) -> List[str]:
        calibration_path = os.path.join(self.granule_href,
                                        "annotation/calibration")
        return [
            os.path.join(calibration_path, x)
            for x in os.listdir(calibration_path)
            if x.endswith("xml") and "calibration" in x
        ]

    @property
    def noise_hrefs(self) -> List[str]:
        calibration_path = os.path.join(self.granule_href,
                                        "annotation/calibration")
        return [
            os.path.join(calibration_path, x)
            for x in os.listdir(calibration_path)
            if x.endswith("xml") and "noise" in x
        ]

    def create_manifest_asset(self):
        asset = pystac.Asset(href=self.href,
                             media_type=pystac.MediaType.XML,
                             roles=["metadata"])
        return (SAFE_MANIFEST_ASSET_KEY, asset)

    def create_product_asset(self):
        assets = []
        for x in self.annotation_hrefs:
            asset = pystac.Asset(
                href=x,
                media_type=pystac.MediaType.XML,
                title="Product Schema",
                roles=["metadata"],
            )
            # Account for different names in SAFE and in Azure
            if len(x.split("/")[-1].split(".")[0].split("-")) > 3:
                assets.append((
                    f"product-{x.split('/')[-1].split('-')[1]}"
                    f"-{x.split('/')[-1].split('-')[3]}",
                    asset,
                ))
            else:
                assets.append(
                    (f"product-{x.split('.')[0].split('/')[-1]}", asset))

        return assets

    def create_calibration_asset(self):
        assets = []
        for x in self.calibration_hrefs:
            asset = pystac.Asset(
                href=x,
                media_type=pystac.MediaType.XML,
                title="Calibration Schema",
                roles=["metadata"],
            )
            # Account for different names in SAFE and in Azure
            if len(x.split("/")[-1].split(".")[0].split("-")) > 3:
                assets.append((
                    f"calibration-{x.split('/')[-1].split('-')[1]}"
                    f"-{x.split('/')[-1].split('-')[3]}",
                    asset,
                ))
            else:
                assets.append((x.split(".")[0].split("/")[-1], asset))

        return assets

    def create_noise_asset(self):
        assets = []
        for x in self.noise_hrefs:
            asset = pystac.Asset(
                href=x,
                media_type=pystac.MediaType.XML,
                title="Noise Schema",
                roles=["metadata"],
            )
            # Account for different names in SAFE and in Azure
            if len(x.split("/")[-1].split(".")[0].split("-")) > 3:
                assets.append((
                    f"calibration-{x.split('/')[-1].split('-')[1]}"
                    f"-{x.split('/')[-1].split('-')[3]}",
                    asset,
                ))
            else:
                assets.append((x.split(".")[0].split("/")[-1], asset))

        return assets
