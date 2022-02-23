"""Bold Smart Lock authentication."""
from __future__ import annotations
from aiohttp.web import HTTPUnauthorized
from bold_smart_lock.exceptions import AuthenticateFailed, EmailOrPhoneNotSpecified, InvalidEmail, InvalidPhone, InvalidValidationCode, InvalidValidationId, InvalidValidationResponse, MissingValidationId, TokenMissing, VerificationNotFound
from .const import (
    API_URI,
    INVALID_EMAIL_ERROR,
    INVALID_PHONE_ERROR,
    POST_HEADERS,
    VALIDATIONS_ENDPOINT,
    AUTHENTICATIONS_ENDPOINT,
)
import aiohttp


class Auth:
    """Authorization class for Bold Smart Lock"""

    def __init__(self, session: aiohttp.ClientSession):
        self._session = session
        self._token: str = None
        self._validation_id: str = None

    async def authenticate(
        self, email: str, password: str, verification_code: str, validation_id: str, language: str = "en"
    ):
        """Authenticate with the login details, validation_id and validation_code"""
        verified = await self.__verify_validation_id(verification_code, validation_id)

        if verified and email and password and self._validation_id:
            request_json = {
                "language": language,
                "clientLocale": "en-US",
                "validationId": self._validation_id,
            }
            headers = self.headers()

            try:
                async with self._session.post(
                    API_URI + AUTHENTICATIONS_ENDPOINT,
                    headers=headers,
                    auth=aiohttp.BasicAuth(email, password),
                    json=request_json,
                    raise_for_status=False
                ) as response:
                    if response.status == 401:
                        raise HTTPUnauthorized
                    elif response.status == 404:
                        raise VerificationNotFound
                    elif response.content_type == "application/json":
                        response_json: dict[str, str] = await response.json()
                        if "token" in response_json:
                            self.set_token(response_json["token"])
                            return response_json
            except Exception as exception:
                raise exception
        raise AuthenticateFailed

    def headers(self, output_text: bool = False):
        """Get the required request headers"""
        headers = {} if output_text else POST_HEADERS
        token = self.token()

        if token:
            headers["X-Auth-Token"] = token
        return headers

    async def re_login(self):
        """Re-login / refresh the token"""
        if self.token():
            async with self._session.put(
                API_URI + AUTHENTICATIONS_ENDPOINT + "/" + self.token(),
                headers=self.headers(),
                raise_for_status=False
            ) as response:
                response_json: dict[str, str] = await response.json()

                if "token" in response_json:
                    self.set_token(response_json["token"])
                    return response_json
        raise TokenMissing

    async def request_validation_id(self, email: str = None, phone: str = None):
        """Request a validation id and receive a validation code by email or phone"""
        request_json = None

        if email:
            request_json = {"email": email}
        elif phone:
            request_json = {"phone": phone}

        if request_json:
            try:
                async with self._session.post(
                    API_URI + VALIDATIONS_ENDPOINT,
                    json=request_json,
                    headers=self.headers(),
                    raise_for_status=False
                ) as response:
                    if response.content_type == "application/json":
                        response_json: dict[str, str] = await response.json()
                        if "errorCode" in response_json:
                            if response_json["errorCode"] == INVALID_EMAIL_ERROR:
                                raise InvalidEmail
                            elif response_json["errorCode"] == INVALID_PHONE_ERROR:
                                raise InvalidPhone
                        elif response_json.status == 400:
                            raise EmailOrPhoneNotSpecified

                        if "id" in response_json:
                            self._validation_id = response_json["id"]
                            return response_json
            except Exception as exception:
                raise exception
        raise EmailOrPhoneNotSpecified

    def set_token(self, token: str):
        """Update the token"""
        self._token = token

    def token(self):
        """Get the token and update it when needed"""
        if self._token:
            return self._token

    async def __verify_validation_id(
        self, verification_code: str, validation_id: str = None
    ) -> bool:
        """Verify an e-mail with the validation_id and validation_code"""
        if validation_id:
            self._validation_id = validation_id

        if self._validation_id and verification_code:
            try:
                async with await self._session.post(
                    API_URI + VALIDATIONS_ENDPOINT + "/" + self._validation_id,
                    json={"code": verification_code},
                    headers=self.headers(),
                    raise_for_status=False
                ) as response:
                    if response.status == 200:
                        return True
                    if response.status == 400:
                        raise InvalidValidationCode
                    elif response.status == 404:
                        raise InvalidValidationId
                    elif response.status == 405:
                        raise MissingValidationId
                    else:
                        raise InvalidValidationResponse
            except Exception as exception:
                raise exception

        return False
