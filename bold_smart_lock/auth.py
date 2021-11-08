"""Bold Smart Lock authentication."""

import aiohttp
from datetime import datetime

from .const import (
    API_URI,
    POST_HEADERS,
    VALIDATIONS_ENDPOINT,
    AUTHENTICATIONS_ENDPOINT,
    AUTHENTICATION_REQUEST_JSON,
)


class Auth:
    """Authorization class for Bold Smart Lock"""

    def __init__(self, session: aiohttp.ClientSession):
        self._session = session
        self._token = None
        self._token_expiration_time = None
        self._validation_id = None

    async def headers(self, output_text: bool = False):
        """Get the required request headers"""

        headers = {} if output_text else POST_HEADERS
        token = await self.token()

        if token:
            headers["X-Auth-Token"] = token

        return headers

    async def request_validation_id(self, email: str):
        """Request a validation_code on the account e-mail"""

        if email:
            headers = await self.headers()

            async with self._session.post(
                API_URI + VALIDATIONS_ENDPOINT, json={"email": email}, headers=headers
            ) as response:
                response_json = await response.json()
                if "id" in response_json:
                    self._validation_id = response_json["id"]
                    return response_json

    async def _verify_validation_id(
        self, verification_code: str, validation_id: str = None
    ) -> bool:
        """Verify an e-mail with the validation_id and validation_code"""

        if validation_id:
            self._validation_id = validation_id

        if self._validation_id and verification_code:
            headers = await self.headers()

            async with self._session.post(
                API_URI + VALIDATIONS_ENDPOINT + "/" + self._validation_id,
                json={"code": verification_code},
                headers=headers,
            ) as response:
                response_json = await response.json()
                if "isVerified" in response_json and response_json["isVerified"]:
                    return True

    async def authenticate(
        self, email: str, password: str, verification_code: str, validation_id: str
    ):
        """Authenticate with the login details, validation_id and validation_code"""

        verified = await self._verify_validation_id(verification_code, validation_id)

        if verified and email and password and self._validation_id:
            request_json = AUTHENTICATION_REQUEST_JSON
            request_json["validationId"] = self._validation_id
            headers = await self.headers()

            async with self._session.post(
                API_URI + AUTHENTICATIONS_ENDPOINT,
                headers=headers,
                auth=aiohttp.BasicAuth(email, password),
                json=request_json,
            ) as response:
                response_json = await response.json()

                if "token" in response_json and "expirationTime" in response_json:
                    self.set_token_data(
                        response_json["token"],
                        datetime.fromisoformat(response_json["expirationTime"][:-1]),
                    )
                    return response_json

    async def token(self) -> str:
        """Get the token and update it when needed"""

        if (
            self._token_expiration_time
            and self._token_expiration_time <= datetime.utcnow()
        ):
            await self.refresh_token()

        if self._token:
            return self._token

    def set_token_data(self, token: str, token_expiration_time: datetime):
        """Update the token and expiration time"""

        self._token = token
        self._token_expiration_time = token_expiration_time

    def refresh_token():
        """Refresh the token"""

        # TODO: implement refresh
        return True
