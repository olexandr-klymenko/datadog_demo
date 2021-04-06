import logging
import os
import traceback
from random import randint, random
from time import sleep

import uvicorn
from datadog import initialize, statsd
from ddtrace import patch, tracer, patch_all
from fastapi import FastAPI

patch(fastapi=True)
patch_all(logging=True)

FORMAT = (
    "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
    "[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s"
    " dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] - %(message)s"
)
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.level = logging.DEBUG

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
