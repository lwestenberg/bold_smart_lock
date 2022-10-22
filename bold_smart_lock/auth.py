"""Authentication library, implemented by users of the API."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional
from aiohttp import ClientError, ClientResponse, ClientSession

_LOGGER = logging.getLogger(__name__)

HTTP_UNAUTHORIZED = 401
AUTHORIZATION_HEADER = "Authorization"
ERROR = "error"
STATUS = "status"
MESSAGE = "message"

class AbstractAuth(ABC):
    """Abstract class to make authenticated requests."""

    def __init__(self, websession: ClientSession, host: str):
        """Initialize the auth."""
        self._websession = websession
        self._host = host

    @abstractmethod
    async def async_get_access_token(self) -> str:
        """Return a valid access token."""

    async def request(
            self, method: str, url: str, **kwargs: Optional[Mapping[str, Any]]
        ) -> ClientResponse:
            """Make a request."""
            headers = kwargs.get("headers")

            if headers is None:
                headers = {}
            else:
                headers = dict(headers)
                del kwargs["headers"]
            if AUTHORIZATION_HEADER not in headers:
                try:
                    access_token = await self.async_get_access_token()
                except ClientError as err:
                    print("error")
                    # raise AuthException(f"Access token failure: {err}") from err
                headers[AUTHORIZATION_HEADER] = f"Bearer {access_token}"
            if not (url.startswith("http://") or url.startswith("https://")):
                url = f"{self._host}/{url}"
            _LOGGER.debug("request[%s]=%s", method, url)
            if method == "post" and "json" in kwargs:
                _LOGGER.debug("request[post json]=%s", kwargs["json"])
            return await self._websession.request(method, url, **kwargs, headers=headers)

    async def get(
        self, url: str, **kwargs: Mapping[str, Any]
    ) -> ClientResponse:
        """Make a get request."""
        try:
            resp = await self.request("get", url, **kwargs)
        except ClientError as err:
            # raise ApiException(f"Error connecting to API: {err}") from err
            print("error")
        return await AbstractAuth._raise_for_status(resp)
