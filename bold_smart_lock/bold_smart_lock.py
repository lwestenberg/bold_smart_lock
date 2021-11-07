import aiohttp
from datetime import datetime

from .const import (
    API_URI,
    REMOTE_ACTIVATION_ENDPOINT,
    EFFECTIVE_DEVICE_PERMISSIONS_ENDPOINT,
)

HEADERS = {'Content-Type' : 'application/json'}

from .auth import Auth

class BoldSmartLock:
    """A Python Abstraction object to Bold Smart Lock"""


    def __init__(self, session: aiohttp.ClientSession):
        """Initialize the Bold Smart Lock object."""
        self._session = session
        self._auth = Auth(session)


    async def verify_email(self, email: str):
        return await self._auth.request_validation_id(email)


    async def authenticate(self, email: str, password: str, verification_code: str, validation_id: str = None):
        return await self._auth.authenticate(email, password, verification_code, validation_id)


    def set_token_data(self, token: str, token_expiration_time: datetime):
        self._auth.set_token_data(token, token_expiration_time)


    async def get_device_permissions(self):
        headers = await self._auth.headers(True)

        async with self._session.get(
            API_URI + EFFECTIVE_DEVICE_PERMISSIONS_ENDPOINT + "?size=1000",
            headers=headers
        ) as response:
            response_text = await response.text()
            return response_text


    async def remote_activation(self, device_id: int):
        headers = await self._auth.headers(True)

        async with self._session.post(
            API_URI + REMOTE_ACTIVATION_ENDPOINT.format(device_id),
            headers=headers
        ) as response:
            response_text = await response.text()
            return response_text
