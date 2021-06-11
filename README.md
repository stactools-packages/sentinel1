# stactools-sentinel1

Template repostitory for [stactools](https://github.com/stac-utils/stactools) packages.

## How to use

1. Clone this repository and name it `stactools-{NAME}`, where `NAME` is your package name.
   This name should be short, memorable, and a valid Python package name (i.e. it shouldn't start with a number, etc).
2. Update `setup.cfg` with your package name, description, and such.
3. Rename `src/stactools.sentinel1` to `src/stactools/{NAME}`.
4. Rewrite this README to provide information about how to use your package.
5. Update the LICENSE with your company's information (or whomever holds the copyright).
6. Update the environment name in `environment.yml`.
7. Update the environment variables in `.github/workflows/release.yml` to the appropriate values to publish for your organization.
8. Update all scripts in the `docker` directory to refer to `stactools-{NAME}` and `stactools-{NAME}-dev`.
