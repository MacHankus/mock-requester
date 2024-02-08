import asyncio
import json
import random
import string
import sys
import time
from pathlib import Path

from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette.responses import PlainTextResponse
from loguru import logger

from definitions import PROJECT_NAME
from ioc_container import Container, wiring_modules
from modules.adapters.api.mock_router import router
from settings import settings
import uuid

APP_FROZEN = getattr(sys, "frozen", False)


async def create_app() -> FastAPI:
    logger.info(f"{PROJECT_NAME} initialization.")

    application = FastAPI(
        title=PROJECT_NAME,
        root_path="/",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    application.logger = logger

    container = Container()
    container.init_resources()

    container.wire(wiring_modules)

    application.container = container

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        logger.error(exc)
        return PlainTextResponse("Validation error", status_code=422)

    return application


app: FastAPI = asyncio.run(create_app())


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    body = await request.body()
    log = (
        f"Start handling request ({request_id}) path=({request.url.path}) "
        f"method=({request.method}) body=({body})"
    )

    query_params = str(request.query_params)
    if len(query_params):
        log += f" query=({query_params})"

    logger.info(log)
    start_time = time.time()
    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(
        f"Finished handling request ({request_id}) completed_in={formatted_process_time}"
        " status_code={response.status_code}"
    )

    return response


app.include_router(router)
