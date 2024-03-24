FROM python:3.10-slim

WORKDIR /app

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1
RUN pip install --upgrade pip==24.0

COPY requirements.txt .
RUN pip install --requirement requirements.txt && \
    rm requirements.txt

COPY src/ /app

ARG PORT=5001
ENV PORT ${PORT}

ENTRYPOINT ["/bin/bash", "-o", "pipefail", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]