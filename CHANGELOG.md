# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project attempts to match the major and minor versions of
[stactools](https://github.com/stac-utils/stactools) and increments the patch
number as needed.

## [Unreleased]

## [0.5.0] - 2023-02-06

### Added

- Added `create-collection` command for `sentinel1 grd` ([#24](https://github.com/stactools-packages/sentinel1/pull/24))

### Changed

- Some variable names in `constants.py` ([#24](https://github.com/stactools-packages/sentinel1/pull/24))

## [0.4.0] - 2023-01-31

### Added

- `kwargs` for IO operations ([#21](https://github.com/stactools-packages/sentinel1/pull/21))

### Changed

- Upgraded core linting and testing to latest from **stactools-template** ([#23](https://github.com/stactools-packages/sentinel1/pull/23))

### Removed

- Python 3.7 support ([#23](https://github.com/stactools-packages/sentinel1/pull/23))

## [0.3.0] - 2022-12-01

### Added

- Add support for remote links and URL signing in GRD package

### Changed

- Make GRD input format selectable via parameter - SAFE (default) or COG
- Rename GRD schema keys to better reflect their contents
- Ensure RTC Items list RasterExtension (#16)

### Fixed

- Temporal extent for the RTC Collection, and some typing ([#17](https://github.com/stactools-packages/sentinel1/pull/17))

## [0.2.0] - 2021-09-09

- Added `stac sentinel1 grd` subcommand
- `stac sentinel1 create-item` now required subcommand `grd` or `rtc`
- Support for Microsoft Azure storage: similar format to SAFE,\
without `.SAFE` ending to the folders and slightly different file names.

## [0.1.0] - 2021-09-04

- Initial release!
- Support for Sentinel1 AWS RTC public dataset

[Unreleased]: https://github.com/stactools-packages/sentinel1/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/stactools-packages/sentinel1/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/stactools-packages/sentinel1/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/stactools-packages/sentinel1/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/stactools-packages/sentinel1/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/stactools-packages/sentinel1/releases/tag/v0.1.0
