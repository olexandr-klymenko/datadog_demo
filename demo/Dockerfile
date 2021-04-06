FROM python

COPY ./requirements.txt /opt/
WORKDIR /opt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY . /opt/
