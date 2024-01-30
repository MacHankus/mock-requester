from typing import Dict

from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import Path
from fastapi import status

from modules.core.ports.request_service_port import RequestServicePort

router = APIRouter()


@router.post("{rest_of_path:path}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def process_post(
    rest_of_path: str = Path(),
    body: Dict = Body(None),
    request_service: RequestServicePort = Depends(Provide["request_service"]),
):
    request_service.make_request(path=rest_of_path, body=body)
