ARG STACTOOLS_VERSION=latest
FROM ghcr.io/stac-utils/stactools:$STACTOOLS_VERSION

WORKDIR /opt/stactools-package

# For caching purposes, install dependencies but remove the actual package
COPY pyproject.toml setup.cfg ./
COPY src/stactools/package/__init__.py src/stactools/package/
RUN pip install . \
    && rm -r /opt/conda/lib/python3.8/site-packages/stactools/package

COPY src ./src
RUN pip install .
