import itertools
import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

import pystac
import stactools.core.io
from lxml import etree
from stactools.core.io import ReadHrefModifier
from stactools.core.io.xml import XmlElement

from .formats import Format
from .grd.constants import SAFE_MANIFEST_ASSET_KEY


class ManifestError(Exception):
    pass


dataset_naming_pattern = re.compile(
    "^.*"
    + "(?P<mission>s1a|s1b)"
    + "-(?P<swath>s[1-6]|iw[1-3]?|ew[1-5]?|wv[1-2]|en|n[1-6]|is[1-7])"
    + "-(?P<type>slc|grd)"
    + "-(?P<polarisation>hh|hv|vv|vh)"
    + "-([0-9]{8}t[0-9]{6})"
    + "-([0-9]{8}t[0-9]{6})"
    + "-([0-9]{6})"
    + "-([0-9a-f]{6})"
    + ".*$"
)


def extract_polarisation(href: str) -> str:
    if match := dataset_naming_pattern.match(href):
        return match.group("polarisation").upper()
    elif match := re.search(r"-(hh|hv|vv|vh)\.(?:tiff|xml)$", href):
        return match.group(1).upper()
    raise RuntimeError(f"Failed to match polarisation: {href}")


def extract_properties(href: str, properties: List[str]) -> List[str]:
    matches = dataset_naming_pattern.match(href)
    if matches is not None:
        return [matches.group(name) for name in properties]
    else:
        raise RuntimeError(f"href doesn't match dataset naming pattern: {href}")


def group_files(hrefs: List[str]) -> Dict[str, List[str]]:
    def determine_group(href: str) -> str:
        if href.startswith("annotation/calibration/calibration"):
            return "calibration_calibration"
        elif href.startswith("annotation/calibration/noise"):
            return "calibration_noise"
        elif href.startswith("annotation"):
            return "annotation"
        elif href.startswith("measurement"):
            return "measurement"
        elif href.startswith("S1"):
            return "other"
        else:
            return "other_short"

    list.sort(hrefs, key=determine_group)

    grouped_hrefs = {}
    for k, v in itertools.groupby(hrefs, determine_group):
        grouped_hrefs[k] = list(v)

    return grouped_hrefs


class MetadataLinks:
    def __init__(
        self,
        granule_href: str,
        read_href_modifier: Optional[ReadHrefModifier] = None,
        archive_format: Format = Format.SAFE,
        **kwargs: Any,
    ) -> None:
        self.granule_href = granule_href
        self.href = os.path.join(granule_href, "manifest.safe")
        self.archive_format = archive_format

        self.manifest = XmlElement.from_file(self.href, read_href_modifier, **kwargs)
        data_object_section = self.manifest.find("dataObjectSection")
        if data_object_section is None:
            raise ManifestError(
                f"Manifest at {self.href} does not have a dataObjectSection"
            )

        self._data_object_section = data_object_section
        self.product_metadata_href = os.path.join(granule_href, "manifest.safe")

        if archive_format == Format.COG:
            self.product_info_href = os.path.join(granule_href, "productInfo.json")
            self.product_info = json.loads(
                stactools.core.io.read_text(
                    self.product_info_href, read_href_modifier, **kwargs
                )
            )
            self.filename_map = self.product_info["filenameMap"]

        file_location_list = self._data_object_section.findall(
            "dataObject/byteStream/fileLocation[@href]"
        )

        def href_finder(el: XmlElement) -> Optional[str]:
            href = el.find_attr("href", ".")
            if href is not None:
                return href.strip("./")
            else:
                raise RuntimeError(
                    f"No href found in XML element {etree.tostring(el.element)}"
                )

        optional_href_list = [href_finder(href) for href in file_location_list]
        href_list = [x for x in optional_href_list if x is not None]

        self.grouped_hrefs = group_files(href_list)

    def map_filename(self, filename: str) -> str:
        if self.archive_format == Format.SAFE:
            return filename
        elif self.archive_format == Format.COG:
            return str(self.filename_map[filename])
        else:
            raise RuntimeError(f"Unknown format encountered: {self.archive_format}")

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
    def annotation_hrefs(self) -> List[Tuple[str, str]]:
        return [
            (
                "schema-product-{}".format(*extract_properties(x, ["polarisation"])),
                os.path.join(self.granule_href, self.map_filename(x)),
            )
            for x in self.grouped_hrefs["annotation"]
            if x.endswith("xml")
        ]

    @property
    def calibration_hrefs(self) -> List[Tuple[str, str]]:
        return [
            (
                "schema-calibration-{}".format(
                    *extract_properties(x, ["polarisation"])
                ),
                os.path.join(self.granule_href, self.map_filename(x)),
            )
            for x in self.grouped_hrefs["calibration_calibration"]
        ]

    @property
    def noise_hrefs(self) -> List[Tuple[str, str]]:
        return [
            (
                "schema-noise-{}".format(*extract_properties(x, ["polarisation"])),
                os.path.join(self.granule_href, self.map_filename(x)),
            )
            for x in self.grouped_hrefs["calibration_noise"]
        ]

    def create_manifest_asset(self) -> Tuple[str, pystac.asset.Asset]:
        desc = (
            "General product metadata in XML format. Contains a high-level textual "
            "description of the product and references to all of product's components, "
            "the product metadata, including the product identification and the resource "
            "references, and references to the physical location of each component file "
            "contained in the product."
        )

        asset = pystac.Asset(
            href=self.href,
            media_type=pystac.MediaType.XML,
            title="Manifest File",
            roles=["metadata"],
            description=desc,
        )
        return SAFE_MANIFEST_ASSET_KEY, asset

    def create_product_asset(self) -> List[Tuple[str, pystac.asset.Asset]]:
        assets = []
        desc = (
            "Describes the main characteristics corresponding to the band: state of the "
            "platform during acquisition, image properties, Doppler information, geographic "
            "location, etc."
        )
        for key, href in self.annotation_hrefs:
            # Extract polarisation from href
            polarisation = extract_polarisation(href)
            if polarisation:
                # Add polarisation to title
                title = f"{polarisation} Product Schema"
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
            polarisation = extract_polarisation(href)
            if polarisation:
                # Add polarisation to title
                title = f"{polarisation} Calibration Schema"
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
            polarisation = extract_polarisation(href)
            if polarisation:
                # Add polarisation to title
                title = f"{polarisation} Noise Schema"
                asset = pystac.Asset(
                    href=href,
                    media_type=pystac.MediaType.XML,
                    title=title,
                    roles=["metadata"],
                    description="Estimated thermal noise look-up tables",
                )
                assets.append((key, asset))
        return assets
