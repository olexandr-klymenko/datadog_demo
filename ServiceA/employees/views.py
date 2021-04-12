from datetime import date
import logging
from os import getenv
from random import randint, random
import traceback
from time import sleep
from typing import List

from ddtrace import tracer
import requests
from datadog import statsd
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema

from .models import Employee, Department

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


class DepartmentIn(Schema):
    title: str


class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int
    birthdate: date


class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int
    birthdate: date


@api.post("/departments")
def create_employee(request, payload: DepartmentIn):
    department = Department.objects.create(**payload.dict())
    return {"id": department.id}


@tracer.wrap()
@api.post("/employees")
def create_employee(request, payload: EmployeeIn):
    return {"id": Employee.objects.create(**payload.dict()).id}


@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    return get_object_or_404(Employee, id=employee_id)


@statsd.timed("django3.views.employees.timer", tags=["function:employees_from_db"])
def employees_from_db():
    sleep(random())
    return Employee.objects.all()


@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    logger.info("Requesting list of employees ...")
    statsd.increment("django3.views.employees.count")
    try:
        if randint(1, 10) == 7:
            raise RuntimeError("ServiceA random runtime error")
        resp = employees_from_db()
    except RuntimeError:
        logger.error("uncaught exception: %s", traceback.format_exc())
        statsd.increment("django3.views.employees_failure.count")
        return False
    else:
        logger.info("Got list of employees.")
        statsd.increment("django3.views.employees_success.count")
        return resp


@api.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}


@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}
