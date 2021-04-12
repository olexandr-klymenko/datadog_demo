import asyncio
import sys
from os import getenv
from random import choice

import httpx

API_URL = getenv("API_URL")

ENDPOINTS = ["service_b/check", "employees", "service_b/check"]

ITERATIONS = int(sys.argv[1])


async def make_request():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_URL}/{choice(ENDPOINTS)}")
        print(resp)


async def main():
    await asyncio.gather(
        *[asyncio.create_task(make_request()) for _ in range(ITERATIONS)]
    )


asyncio.run(main())
