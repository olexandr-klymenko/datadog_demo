FROM python:3.8-slim

COPY ./requirements.txt /srv/
WORKDIR /srv
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY app /srv/app
