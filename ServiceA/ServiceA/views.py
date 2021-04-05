from os import getenv

import requests
from ninja import NinjaAPI

api = NinjaAPI()


@api.get("/info")
def info(request):
    return {"title": "DJango3.1"}


@api.get("/serviceb/info")
def serviceb_info(request):
    return requests.get(f"{getenv('SERVICE_B_URL')}/info").json()
