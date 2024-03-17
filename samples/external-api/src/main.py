from datetime import datetime
from uvicorn import run
from typing import Dict, List

from fastapi import Body, FastAPI
from pydantic import BaseModel
from starlette import status

import os
from loguru import logger

app = FastAPI()

DB = []

APP_NAME = os.environ.get("APP_NAME")
if not APP_NAME:
    raise ValueError("APP_NAME should be provided.")


class SaveModel(BaseModel):
    request_id: str
    body: Dict | None


@app.post("/save", response_model=SaveModel, status_code=status.HTTP_200_OK)
def root(
    payload: Dict = Body(
        None,
    )
):
    logger.info(f"{APP_NAME} is handling `/save` request.")
    request_id = datetime.now().isoformat()
    result = {"request_id": request_id, "body": payload}
    DB.append(result)
    return result


class RequestHistoryModel(BaseModel):
    app_name: str = APP_NAME
    history: List[SaveModel]


@app.get(
    "/request-history",
    response_model=RequestHistoryModel,
    status_code=status.HTTP_200_OK,
)
def root():
    response = RequestHistoryModel(history=DB)
    return response


run(app, host="0.0.0.0")
