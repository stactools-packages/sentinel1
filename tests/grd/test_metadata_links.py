from stactools.sentinel1.grd.metadata_links import extract_polarisation


def test_extract_polarization() -> None:
    paths_to_polarization = {
        "S1A_IW_GRDH_1SDV_20210809T173953_20210809T174018_039156_049F13_6FF8.SAFE/measurement/s1a-iw-grd-vh-20210809t173953-20210809t174018-039156-049f13-002.tiff": "VH",  # noqa: E501
        "S1A_IW_GRDH_1SDV_20210809T173953_20210809T174018_039156_049F13_6FF8.SAFE/measurement/s1a-iw-grd-vv-20210809t173953-20210809t174018-039156-049f13-001.tiff": "VV",  # noqa: E501
        "S1A_IW_GRDH_1SDV_20210809T173953_20210809T174018_039156_049F13_6FF8.SAFE/measurement/s1a-iw-grd-hh-20210809t173953-20210809t174018-039156-049f13-001.tiff": "HH",  # noqa: E501
        "S1A_IW_GRDH_1SDV_20210809T173953_20210809T174018_039156_049F13_6FF8.SAFE/measurement/s1a-iw-grd-hv-20210809t173953-20210809t174018-039156-049f13-001.tiff": "HV",  # noqa: E501
        "S1A_EW_GRDM_1SDH_20221130T014342_20221130T014446_046117_058549_BB15/measurement/ew-hh.tiff": "HH",  # noqa: E501
        "S1A_EW_GRDM_1SDH_20221130T014342_20221130T014446_046117_058549_BB15/measurement/ew-hv.tiff": "HV",  # noqa: E501
        "S1A_EW_GRDM_1SDH_20221130T014342_20221130T014446_046117_058549_BB15/measurement/ew-vv.tiff": "VV",  # noqa: E501
        "S1A_EW_GRDM_1SDH_20221130T014342_20221130T014446_046117_058549_BB15/measurement/ew-vh.tiff": "VH",  # noqa: E501
    }

    # initially, the extract_polarization looked for the two-letter polarization anywhere
    # in the path, which led to many false-detections in temp directories
    for test_polarization in ["vv", "vh", "hv", "hh"]:
        for path, expected_polarization in paths_to_polarization.items():
            assert (
                extract_polarisation(f"some_path/xx{test_polarization}yy/{path}")
                == expected_polarization
            )
