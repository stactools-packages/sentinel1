ARG STACTOOLS_VERSION=latest
FROM ghcr.io/stac-utils/stactools:$STACTOOLS_VERSION

WORKDIR /opt/stactools-sentinel1

# For caching purposes, install dependencies but remove the actual package
COPY pyproject.toml setup.cfg ./
COPY src/stactools/sentinel1/__init__.py src/stactools/sentinel1/
RUN pip install . \
    && rm -r /opt/conda/lib/python3.8/site-packages/stactools/sentinel1

COPY src ./src
RUN pip install .
