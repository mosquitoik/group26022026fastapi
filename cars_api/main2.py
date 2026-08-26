from fastapi import FastAPI

from cars_api.api_router2 import api_router


app = FastAPI(
    title="Cars FAST API",
)

app.include_router(api_router, tags=["CARS"])
