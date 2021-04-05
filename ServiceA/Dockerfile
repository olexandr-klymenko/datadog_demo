FROM python

COPY ./requirements.txt /srv/
WORKDIR /srv
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY . /srv
