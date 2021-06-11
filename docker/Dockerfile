FROM continuumio/miniconda3

RUN conda update conda && conda install pip

COPY environment.yml /tmp/environment.yml
RUN conda env update -f /tmp/environment.yml -n base && rm /tmp/environment.yml

COPY . /tmp/stactools-sentinel1
RUN cd /tmp/stactools-sentinel1 && pip install . && rm -rf /tmp/stactools-sentinel1

ENTRYPOINT [ "python", "-m", "stactools.cli" ]
