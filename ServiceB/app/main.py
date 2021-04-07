import logging
import os
import traceback
from random import randint, random
from time import sleep

import uvicorn
from datadog import initialize, statsd
from ddtrace import patch, tracer, patch_all
from fastapi import FastAPI
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

patch(fastapi=True)
patch_all(logging=True)

initialize(statsd_host=os.getenv("DATADOG_HOST"), statsd_port=8125)
tracer.configure(hostname=os.getenv("DATADOG_HOST"), port=8126, enabled=True)

app = FastAPI()


@statsd.timed("fastapi.views.check.timer", tags=["function:do_check"])
def do_check():
    sleep(random())


@app.get("/check")
def check():
    statsd.increment("fastapi.views.check.count")
    logger.info("ServiceB check")
    try:
        if randint(1, 12) == 7:
            raise RuntimeError("ServiceB random runtime error")
        do_check()
        return {"message": "success"}
    except RuntimeError:
        logger.exception("uncaught exception: %s", traceback.format_exc())
        raise


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
