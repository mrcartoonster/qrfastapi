# -*- coding: utf-8 -*-
# project/app/main.py
"""
This is where our FastAPI endpoint routers from sponsors and beers are
served.
"""
import sentry_sdk
from fastapi import FastAPI
from environs import ENV

from app.api import beer
from app.db import init_db

from .desc import desc

env = ENV()
env.read_env()


sentry_sdk.init(
    env('SENTRY'),
    traces_sample_rate=1.0
)


def create_app() -> FastAPI:
    """
    FastAPI app factory.
    """

    # FastAPI instance
    app = FastAPI(
        title="OpenBrewery",
        description=desc,
        version="0.0.1",
        redoc_url="/",
    )

    # API endpoints
    app.include_router(beer.router, prefix="/breweries", tags=["beer"])

    return app


app = create_app()


@app.on_event("startup")
async def startup():
    """
    Starting up tortoise for FastAPI.
    """
    init_db(app)


@app.on_event("shutdown")
async def shutdown():
    """
    Proper shutdown of Tortoise and Event loop.
    """
    ...
