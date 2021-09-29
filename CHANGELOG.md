# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). This project attempts to match the major and minor versions of [stactools](https://github.com/stac-utils/stactools) and increments the patch number as needed.

## [v0.2.1] - 2021-09-29
### Added
- Add support for remote links and URL signing in GRD package
### Changed
- Make GRD input format selectable via parameter - SAFE (default) or COG
- Rename GRD schema keys to better reflect their contents

## [v0.2.0] - 2021-09-09

- Added `stac sentinel1 grd` subcommand
- `stac sentinel1 create-item` now required subcommand `grd` or `rtc`
- Support for Microsoft Azure storage: similar format to SAFE, without `.SAFE` ending to the folders and slightly different file names.

## [v0.1.0] - 2021-09-04

- Initial release!
- Support for Sentinel1 AWS RTC public dataset
