from datetime import date
import logging
from os import getenv
from random import randint
import traceback
from typing import List

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
    statsd.increment("django3.views.check")
    try:
        return requests.get(f"{getenv('SERVICE_B_URL')}/check").json()
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
        raise


class DepartmentIn(Schema):
    title: str


class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None


class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None


@api.post("/departments")
def create_employee(request, payload: DepartmentIn):
    department = Department.objects.create(**payload.dict())
    return {"id": department.id}


@api.post("/employees")
def create_employee(request, payload: EmployeeIn):
    return {"id": Employee.objects.create(**payload.dict()).id}


@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    return get_object_or_404(Employee, id=employee_id)


@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    logger.debug("List of employees")
    try:
        if randint(1, 10) == 7:
            raise RuntimeError("ServiceA random runtime error")
        return Employee.objects.all()
    except RuntimeError:
        logger.error("uncaught exception: %s", traceback.format_exc())
        return False


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
