FROM python

ENV DD_SERVICE fastapi
ENV DD_VERSION 1.0

LABEL com.datadoghq.tags.service="fastapi"
LABEL com.datadoghq.tags.version="1.0"

COPY ./requirements.txt /srv/
WORKDIR /srv
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY app /srv/app
