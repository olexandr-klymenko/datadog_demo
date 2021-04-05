import logging
import os

import uvicorn
from datadog import initialize, statsd
from ddtrace import patch, tracer
from fastapi import FastAPI

patch(fastapi=True)

initialize(statsd_host=os.getenv('DATADOG_HOST'))

logger = logging.getLogger(__name__)

app = FastAPI()

tracer.configure(hostname=os.getenv("DATADOG_HOST"), port=8126, enabled=True)


@app.get("/info")
def info():
    statsd.increment('fastapi.views.info')
    return {"title": "FastAPI"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)
