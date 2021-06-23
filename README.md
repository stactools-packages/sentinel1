# stactools-sentinel1
[![CI](https://github.com/stactools-packages/sentinel1/actions/workflows/continuous-integration.yml/badge.svg)](https://github.com/stactools-packages/sentinel1/actions/workflows/continuous-integration.yml)

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
```

Make changes on a new branch, test, open a pull request
```
git checkout -b newfeature
git commit -a -m "fixed some metadata issue"
python -m unittest discover tests
```
