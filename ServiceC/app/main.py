import json
import logging
import os

import sqlalchemy as db
import zope.sqlalchemy
from asgiref.wsgi import WsgiToAsgi
from datadog import initialize
from ddtrace import tracer, patch
from ddtrace.contrib.pyramid import trace_pyramid
from pyramid.config import Configurator
from pyramid.response import Response
from sqlalchemy.orm import sessionmaker, configure_mappers

from app import models
from log_formatter import CustomJsonFormatter

configure_mappers()


class CustomLogger(logging.Logger):
    propagate = False


logger = CustomLogger("pyramid")

logHandler = logging.StreamHandler()
formatter = CustomJsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

settings = {
    "datadog_trace_service": "datadog_demo_pyramid",
}


def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def get_tm_session(session_factory, transaction_manager):
    """
    Get a ``sqlalchemy.orm.Session`` instance backed by a transaction.

    This function will hook the session to the transaction manager which
    will take care of committing any changes.

    - When using pyramid_tm it will automatically be committed or aborted
      depending on whether an exception is raised.

    - When using scripts you should wrap the session in a manager yourself.
      For example::

          import transaction

          engine = get_engine(settings)
          session_factory = get_session_factory(engine)
          with transaction.manager:
              dbsession = get_tm_session(session_factory, transaction.manager)

    """
    dbsession = session_factory()
    zope.sqlalchemy.register(
        dbsession, transaction_manager=transaction_manager)
    return dbsession


def employees(request):
    logger.info("Querying SQLite database for list of employees ...")
    res = request.dbsession.query(models.Employee).all()
    response = Response(json.dumps({"employees": res}))
    response.status = "200 OK"
    response.status_int = 200
    response.content_type = "application/json"
    response.charset = "utf-8"
    return response


with Configurator(settings=settings) as pyramid_config:
    pyramid_config.add_route("employees", "/employees")
    pyramid_config.add_view(employees, route_name="employees")

    engine = db.create_engine("sqlite:///employees.db")
    models.initialize_sql(engine)
    session_factory = get_session_factory(engine)
    pyramid_config.registry['dbsession_factory'] = session_factory

    pyramid_config.include('pyramid_tm')
    pyramid_config.include('pyramid_retry')
    pyramid_config.add_request_method(
        lambda r: get_tm_session(session_factory, r.tm),
        'dbsession',
        reify=True
    )

    initialize(
        statsd_host=os.getenv("DATADOG_HOST"), statsd_port=8125, host_name="pyramid"
    )
    tracer.configure(hostname=os.getenv("DATADOG_HOST"), port=8126, enabled=True)
    trace_pyramid(pyramid_config)
    patch(sqlalchemy=True, logging=True, sqlite3=True)
    wsgi_app = pyramid_config.make_wsgi_app()

app = WsgiToAsgi(wsgi_app)
