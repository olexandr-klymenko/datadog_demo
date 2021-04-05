import logging

import uvicorn
from fastapi import FastAPI

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/info")
def rpc():
    return {"title": "FastAPI"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)
