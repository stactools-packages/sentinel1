ARG STACTOOLS_VERSION=latest
FROM ghcr.io/stac-utils/stactools:$STACTOOLS_VERSION

ARG DOCKER_NAMESPACE_PACKAGE_DIR
ARG DOCKER_WORKDIR
ENV PYTHON_VERSION=3.11
WORKDIR $DOCKER_WORKDIR

# For caching purposes, install dependencies but remove the actual package
COPY pyproject.toml ./
COPY src/$DOCKER_NAMESPACE_PACKAGE_DIR/__init__.py src/$DOCKER_NAMESPACE_PACKAGE_DIR/
RUN pip install . --no-binary rasterio \
    && rm -r /opt/conda/lib/python$PYTHON_VERSION/site-packages/$DOCKER_NAMESPACE_PACKAGE_DIR

COPY src ./src
RUN git init
RUN pip install . --no-binary rasterio
