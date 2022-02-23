"""Bold Smart Lock API wrapper"""
from __future__ import annotations
from .auth import Auth
from .const import (
    API_URI,
    REMOTE_ACTIVATION_ENDPOINT,
    EFFECTIVE_DEVICE_PERMISSIONS_ENDPOINT,
)
import aiohttp

class BoldSmartLock:
    """A Python Abstraction object to Bold Smart Lock"""

    def __init__(self, session: aiohttp.ClientSession):
        """Initialize the Bold Smart Lock object."""
        self._session = session
        self._auth = Auth(session)

    async def authenticate(
        self,
        email: str,
        password: str,
        validation_code: str,
        validation_id: str = None,
    ):
        """Authenticate with account data, validation id and validation code"""
        return await self._auth.authenticate(
            email, password, validation_code, validation_id
        )

    async def get_device_permissions(self):
        """Get the device data and permissions"""
        headers = self._auth.headers(True)

        try:
            async with self._session.get(
                API_URI + EFFECTIVE_DEVICE_PERMISSIONS_ENDPOINT, headers=headers, raise_for_status=True
            ) as response:
                response_json: dict[str, str] = await response.json()
                return response_json
        except Exception as exception:
            raise exception

    async def re_login(self):
        """Re-login / refresh token"""
        return await self._auth.re_login()

    async def remote_activation(self, device_id: int):
        """Activate the device remotely"""
        headers = self._auth.headers(True)

        try:
            async with self._session.post(
                API_URI + REMOTE_ACTIVATION_ENDPOINT.format(device_id), headers=headers, raise_for_status=True
            ) as response:
                response_json: dict[str, str] = await response.json()
                return response_json
        except Exception as exception:
            raise exception

    def set_token(self, token: str):
        """Set the token"""
        self._auth.set_token(token)

    async def request_validation_id(self, email: str = None, phone: str = None):
        """Request a validation id and receive a validation code by e-mail or phone"""
        return await self._auth.request_validation_id(email, phone)

