from typing import Dict

import httpx
from loguru import logger

from modules.core.enums.http import HttpMethodsEnum
from modules.core.exceptions.service_unavailable_error import ServiceUnavailableError
from modules.core.ports.request_maker_port import RequestMakerPort


class RequestMaker(RequestMakerPort):
    def __init__(self) -> None:
        self.client = httpx.Client(event_hooks={"request": [self._log_before_request]})

    def _log_before_request(self, request: httpx.Request) -> None:
        logger.debug(
            f"Sending request to {str(request.url)} with body "
            f"({str(request.content)}) and headers ({str(request.headers)})"
        )

    def make(
        self,
        url: str,
        method: HttpMethodsEnum,
        payload: Dict | None = None,
        headers: Dict | None = None,
    ) -> None:
        if method == HttpMethodsEnum.POST:
            request_method = self.client.post
        elif method == HttpMethodsEnum.GET:
            request_method = self.client.get
        elif method == HttpMethodsEnum.PUT:
            request_method = self.client.put
        logger.info(
            f"Parameters in request url={url}, method={method}, payload={payload}, headers={headers}"
        )
        try:
            response = request_method(
                url=url,
                json=payload,
                headers=headers,
            )
        except httpx.RequestError:
            logger.exception("Exception during request")
            raise ServiceUnavailableError()

        logger.info("-------------------------------")
        logger.info(f"Target responded with: {response}")
        return None
