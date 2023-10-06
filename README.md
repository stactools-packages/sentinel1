# stactools-sentinel1

[![CI](https://github.com/stactools-packages/sentinel1/actions/workflows/continuous-integration.yml/badge.svg)](https://github.com/stactools-packages/sentinel1/actions/workflows/continuous-integration.yml)
![PyPI](https://img.shields.io/pypi/v/stactools-sentinel1)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/stactools-packages/sentinel1/main?filepath=docs/installation_and_basic_usage.ipynb)

- Name: sentinel1
- Package: `stactools.sentinel1`
- PyPI: <https://pypi.org/project/stactools-sentinel1/>
- Owners: @scottyhq (RTC), @maximlamare (GRD)
- Dataset homepages:
  - [RTC](https://registry.opendata.aws/sentinel-1-rtc-indigo/)
  - [GRD](https://registry.opendata.aws/sentinel-1/)
- STAC extensions used:
  - [projection](https://github.com/stac-extensions/projection/)
  - [sar](https://github.com/stac-extensions/sar)
  - [sat](https://github.com/stac-extensions/sat)
  - [raster](https://github.com/stac-extensions/raster)
  - [mgrs](https://github.com/stac-extensions/mgrs)
  - [processing](https://github.com/stac-extensions/processing)

Sentinel-1 subpackage for [stactools](https://github.com/stac-utils/stactools)

This project contains multiple subpackages that work with different Sentinel 1
data products.

## RTC

The `stactools.sentinel1.rtc` subpackage and `stac sentinel1 rtc` commands deal
with the Sentinel 1 Radiometric Terrain Corrected (RTC) data hosted on AWS and
produced by Indigo Ag. This data was processed from original Ground Range
Detected (GRD) scenes into a Radiometrically Terrain Corrected, tiled product
suitable for analysis.

See <https://registry.opendata.aws/sentinel-1-rtc-indigo> for more information
about this dataset.

## GRD

The `stactools.sentinel1.grd` subpackage and `stac sentinel1 grd` commands deal
with [Sentinel 1 Ground Range Detected (GRD)
Level-1](https://sentinel.esa.int/web/sentinel/user-guides/sentinel-1-sar/resolutions/level-1-ground-range-detected)
product. It is used to create STAC Items from the SAFE manifest format of the
data hosted on Microsoft Azure.

## SLC

The `stactools.sentinel1.slc` subpackage and `stac sentinel1 slc` commands deal
with [Sentinel 1 Single Look Complex (SLC)
Level-1](https://sentinel.esa.int/web/sentinel/user-guides/sentinel-1-sar/resolutions/level-1-single-look-complex)
product.

## Example Outputs

### RTC

- [Collection](examples/rtc/sentinel1-rtc-aws/collection.json)
- [Item (S1B_20161121_12SYJ_ASC)](examples/rtc/sentinel1-rtc-aws/2016/S1B_20161121_12SYJ_ASC/S1B_20161121_12SYJ_ASC.json)
- [Item (S1A_20200103_17RMJ_ASC)](examples/rtc/sentinel1-rtc-aws/2020/S1A_20200103_17RMJ_ASC/S1A_20200103_17RMJ_ASC.json)

### GRD

- [Item (S1A_EW_GRDM_1SDH_20221130T014342_20221130T014446_046117_058549)](examples/grd/S1A_EW_GRDM_1SDH_20221130T014342_20221130T014446_046117_058549/S1A_EW_GRDM_1SDH_20221130T014342_20221130T014446_046117_058549.json)
- [Item (S1A_IW_GRDH_1SDV_20210809T173953_20210809T174018_039156_049F13)](examples/grd/S1A_IW_GRDH_1SDV_20210809T173953_20210809T174018_039156_049F13/S1A_IW_GRDH_1SDV_20210809T173953_20210809T174018_039156_049F13.json)

### SLC

- [Collection](examples/slc/collection.json)
- [Item (S1A_IW_SL1__1_SH_20141031T095929_20141031T100002_003072_003842)](examples/slc/S1A_IW_SL1__1_SH_20141031T095929_20141031T100002_003072_003842/S1A_IW_SL1__1_SH_20141031T095929_20141031T100002_003072_003842.json)

## How to use

### Install package

```shell
pip install stactools-sentinel1
```

### RTC usage

#### Create a STAC Item (RTC)

<!-- markdownlint-disable MD013 -->
```shell
stac sentinel1 rtc create-item \
  s3://sentinel-s1-rtc-indigo/tiles/RTC/1/IW/12/S/YJ/2016/S1B_20161121_12SYJ_ASC \
  S1B_20161121_12SYJ_ASC
```
<!-- markdownlint-restore -->

#### Create a STAC Static Catalog (RTC)

<https://github.com/scottyhq/sentinel1-rtc-stac>

### GRD usage

Description of the command line functions

```bash
stac sentinel1 grd create-item source destination
```

Use `stac sentinel1 grd --help` to see all subcommands and options.

### SLC usage

Description of the command line functions

```bash
stac sentinel1 slc create-item source destination
```

Use `stac sentinel1 slc --help` to see all subcommands and options.

## Development instructions

### Set up virtual environment

```shell
git clone https://github.com/YOUR_FORK/sentinel1
# Use a virtual environment
conda env create
conda activate stactools-sentinel1
# Development install of dependencies
pip install -e ./
pip install -r requirements-dev.txt
```

### Make changes on a new branch, test, open a pull request

```shell
git checkout -b newfeature
# make changes

# Run CI tests locally
./scripts/cibuild

# Or run individual scripts
./scripts/lint
./scripts/format
./scripts/test

# If you're changing the output STAC metadata, update the examples
./scripts/create_examples.py

# Once tests pass, commit changes and create a pull request
```
