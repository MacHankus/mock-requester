from typing import Dict, MutableMapping

from pydantic import BaseModel


class SideEffectResultEntity(BaseModel):
    payload: Dict | None = None
    headers: MutableMapping | None = None
    cookies: MutableMapping | None = None
    status_code: int