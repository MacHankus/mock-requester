from typing import Dict

from pydantic import BaseModel


class SideEffectResultEntity(BaseModel):
    payload: Dict | None = None
    headers: Dict | None = None
    cookies: Dict | None = None
    status_code: int