"""Request and verify validation codes"""

from aiohttp import ClientSession

from bold_smart_lock.const import API_URI, VERIFICATION_SERVICE
from bold_smart_lock.exceptions import  MissingEmailAddressOrPhoneNumber, MissingVerificationCode


async def request_code(session: ClientSession, emailAddress: str = None, phoneNumber: str = None):
    """Request a validation code. In the request entity, either phone or email must be present."""

    request_json = None

    if emailAddress:
        request_json = {
            "emailAddress": emailAddress,
            "destination": "email"
        }
    elif phoneNumber:
        request_json = {
            "phone": phoneNumber,
            "destination": "phone"
        }

    if request_json:
        try:
            async with session.post(
                API_URI + VERIFICATION_SERVICE + "/request-code",
                json=request_json
            ) as response:
                if response.content_type == "application/json":
                    return await response.json()
        except Exception as exception:
            raise exception
    raise MissingEmailAddressOrPhoneNumber


async def verify_code(session: ClientSession, verificationCode: str, emailAddress: str = None, phoneNumber: str = None):
    """Verify a validation code. In the verification entity, either phone or email must be present."""

    request_json = None

    if not verificationCode:
        raise MissingVerificationCode

    if emailAddress:
        request_json = {
            "emailAddress": emailAddress,
            "destination": "email",
            "verificationCode": verificationCode
        }
    elif phoneNumber:
        request_json = {
            "phone": phoneNumber,
            "destination": "phone",
            "verificationCode": verificationCode
        }

    if request_json:
        try:
            async with session.post(
                API_URI + VERIFICATION_SERVICE + "/verify-code",
                json=request_json
            ) as response:
                if response.content_type == "application/json":
                    return await response.json()
        except Exception as exception:
            raise exception
    raise MissingEmailAddressOrPhoneNumber
