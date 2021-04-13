import json
import logging
import os

from asgiref.wsgi import WsgiToAsgi
from datadog import initialize
from ddtrace import tracer, patch_all
from ddtrace.contrib.pyramid import trace_pyramid
from pyramid.config import Configurator
from pyramid.response import Response

from log_formatter import CustomJsonFormatter


class CustomLogger(logging.Logger):
    propagate = False


logger = CustomLogger("pyramid")

logHandler = logging.StreamHandler()
formatter = CustomJsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

settings = {
    "datadog_trace_service": "pyramid",
}


def hello_world(request):
    logger.info("ServiceC check")
    response = Response(json.dumps({"message": "success"}))
    response.status = "200 OK"
    response.status_int = 200
    response.content_type = "application/json"
    response.charset = "utf-8"
    return response


# Configure a normal WSGI app then wrap it with WSGI -> ASGI class

with Configurator(settings=settings) as config:
    config.add_route("hello", "/")
    config.add_view(hello_world, route_name="hello")
    initialize(statsd_host=os.getenv("DATADOG_HOST"), statsd_port=8125, host_name="pyramid")
    tracer.configure(hostname=os.getenv("DATADOG_HOST"), port=8126, enabled=True)
    trace_pyramid(config)
    patch_all(logging=True)
    wsgi_app = config.make_wsgi_app()

app = WsgiToAsgi(wsgi_app)
