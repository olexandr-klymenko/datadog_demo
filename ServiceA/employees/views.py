import logging
import traceback
from os import getenv

import requests
from datadog import statsd
from django.http import HttpRequest
from ninja import NinjaAPI

logger = logging.getLogger("ServiceA")

api = NinjaAPI()


@api.get("/service_b/check")
def service_b_check(request: HttpRequest):
    url = f"{getenv('SERVICE_B_URL')}/check"
    logger.info("Cross service request to '%s'", url)
    statsd.increment("django3.views.check.count")
    try:
        resp = requests.get(url).json()
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
        statsd.increment("django3.views.check_failure.count")
        raise
    else:
        logger.info("Got response from '%s'", url)
        statsd.increment("django3.views.check_success.count")
        return resp


@api.get("/service_c/employees")
def service_c_employees(request: HttpRequest):
    url = f"{getenv('SERVICE_C_URL')}/employees"
    logger.info("Cross service request to '%s'", url)
    try:
        resp = requests.get(url).json()
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
        raise
    else:
        logger.info("Got response from '%s'", url)
        return resp
