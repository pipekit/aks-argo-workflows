FROM python:3.13 AS base

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir nats-py aiobotocore[awscli]

FROM base AS create

COPY create.py /create.py
ENTRYPOINT ["python", "/create.py"]

FROM base AS dispatch

COPY dispatch.py /dispatch.py
ENTRYPOINT ["python", "/dispatch.py"]

FROM base AS wait

COPY wait.py /wait.py
ENTRYPOINT ["python", "/wait.py"]

FROM base AS consume

COPY consume.py /consume.py
ENTRYPOINT ["python", "/consume.py"]
