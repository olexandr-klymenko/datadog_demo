import asyncio
import sys
from os import getenv
from random import choice

import httpx

API_URL = getenv("API_URL")

ENDPOINTS = ["employees", "service_b/check", "service_c/check"]

TASKS_NUMBER = 100
ITERATIONS = int(sys.argv[1])


async def make_request():
    async with httpx.AsyncClient() as client:
        _ = await client.get(f"{API_URL}/{choice(ENDPOINTS)}")
        print(".", end="")


async def main():
    await asyncio.gather(
        *[asyncio.create_task(make_request()) for _ in range(TASKS_NUMBER)]
    )
    print()


for idx, _ in enumerate(range(ITERATIONS)):
    print(f"Iteration {idx+1}")
    asyncio.run(main())
