FROM mambaorg/micromamba:2.0.5 AS builder

ENV CONDA_ENV_PATH="/opt/conda/envs/starthack"
ENV PATH="$CONDA_ENV_PATH/bin:$PATH"

USER root
COPY environment.yml /tmp/environment.yml

RUN micromamba create -y -f /tmp/environment.yml --prefix $CONDA_ENV_PATH &&  \
micromamba clean --all --yes

WORKDIR /starthack
COPY setup.py /starthack
COPY api /starthack/api
COPY clients /starthack/clients
COPY controllers /starthack/controllers
COPY shared /starthack/shared

RUN python -m pip install -e .

FROM mambaorg/micromamba:2.0.5-debian12-slim AS runtime

USER root
RUN groupadd -g 1000 starthack-group && useradd -m -u 1000 -g 1000 starthack

USER root
WORKDIR /starthack
ENV CONDA_ENV_PATH="/opt/conda/envs/starthack"
ENV PATH="$CONDA_ENV_PATH/bin:$PATH"

COPY --from=builder /opt/conda /opt/conda
COPY setup.py /starthack
COPY api /starthack/api
COPY clients /starthack/clients
COPY controllers /starthack/controllers
COPY shared /starthack/shared
COPY data /starthack/data


CMD ["micromamba", "run", "-n", "starthack", "python", "./api/main.py"]