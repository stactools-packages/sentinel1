# stactools-sentinel1
[![CI](https://github.com/stactools-packages/sentinel1/actions/workflows/continuous-integration.yml/badge.svg)](https://github.com/stactools-packages/sentinel1/actions/workflows/continuous-integration.yml)


- Name: sentinel1
- Package: `stactools.sentinel1`
- PyPI: https://pypi.org/project/stactools-sentinel1/
- Owner: @scottyhq
- Dataset homepage: https://registry.opendata.aws/sentinel-1-rtc-indigo/
- STAC extensions used:
  - [projection](https://github.com/stac-extensions/projection/)
  - [sar](https://github.com/stac-extensions/sar)
  - [sat](https://github.com/stac-extensions/sat)
  - [raster](https://github.com/stac-extensions/raster)
  - [mgrs](https://github.com/stac-extensions/mgrs)
  - [processing](https://github.com/stac-extensions/processing)
- Extra fields:
  - `package:custom`: A custom attribute

A short description of the package and its usage.


Sentinel-1 subpackage for [stactools](https://github.com/stac-utils/stactools)

**NOTE** Currently only configured for AWS Radiometric Terrain Corrected (RTC) Public Dataset: https://registry.opendata.aws/sentinel-1-rtc-indigo. Future versions may support other public datasets such as [GRD and SLC](https://registry.opendata.aws/sentinel-1/).

## How to use

Install package
```
pip install stactools-sentinel1
```

Create a STAC Item
```
stac sentinel1 create-item s3://sentinel-s1-rtc-indigo/tiles/RTC/1/IW/12/S/YJ/2016/S1B_20161121_12SYJ_ASC S1B_20161121_12SYJ_ASC
```

## Development instructions

Set up development conda environment
```
git clone https://github.com/YOUR_FORK/sentinel1
cd sentinel1
conda env create
conda activate stactools-sentinel1
pip install -e ./
pip install -r requirements-dev.txt
```

Make changes on a new branch, test, open a pull request
```
git checkout -b newfeature
# make changes
./scripts/lint
./scripts/format
./scripts/test
```
