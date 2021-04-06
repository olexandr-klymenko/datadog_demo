import logging
import os
import traceback
from random import randint, random
from time import sleep

import json_log_formatter
import uvicorn
from datadog import initialize, statsd
from ddtrace import patch, tracer, patch_all
from fastapi import FastAPI

patch(fastapi=True)
patch_all(logging=True)

formatter = json_log_formatter.JSONFormatter()
json_handler = logging.StreamHandler()
json_handler.setFormatter(formatter)

logger = logging.getLogger('fastapi')
logger.addHandler(json_handler)
logger.setLevel(logging.DEBUG)

initialize(statsd_host=os.getenv("DATADOG_HOST"))

app = FastAPI()

tracer.configure(hostname=os.getenv("DATADOG_HOST"), port=8126, enabled=True)


@tracer.wrap()
@app.get("/check")
def check():
    statsd.increment("fastapi.views.check")
    logger.info("ServiceB check")
    try:
        if randint(1, 10) == 7:
            raise RuntimeError("ServiceB random runtime error")
        sleep(random())
        return {"message": "success"}
    except RuntimeError:
        logger.exception("uncaught exception: %s", traceback.format_exc())
        raise


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
