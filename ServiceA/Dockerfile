FROM python

ENV DD_SERVICE datadog_demo_django3
ENV DD_VERSION 1.0

LABEL com.datadoghq.tags.service="datadog_demo_django3"
LABEL com.datadoghq.tags.version="1.0"

COPY ./requirements.txt /srv/
COPY ./log_formatter.py /srv/
WORKDIR /srv
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY . /srv
