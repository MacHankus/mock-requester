from typing import Callable, Dict

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
            f"({str(request.content)}), headers ({str(request.headers)})"
        )

    def make(
        self,
        url: str,
        method: HttpMethodsEnum,
        payload: Dict | None = None,
        headers: Dict | None = None,
        params: Dict | None = None,
    ) -> None:
        logger.info(f"Got request for url: ({url})")
        request_method: Callable | None = None
        request_params: Dict = dict(
            url=url, json=payload, headers=headers, params=params
        )
        if method == HttpMethodsEnum.POST:
            request_method = self.client.post
        elif method == HttpMethodsEnum.GET:
            request_method = self.client.get
            del request_params["json"]
        elif method == HttpMethodsEnum.PUT:
            request_method = self.client.put

        logger.info(
            f"Parameters in request method={method}, payload={payload}, headers={headers}, params={params}"
        )
        try:
            response = request_method(**request_params)
        except httpx.RequestError:
            logger.exception("Exception during request")
            raise ServiceUnavailableError()

        logger.info(f"Target responded with: {response}")
        return None
