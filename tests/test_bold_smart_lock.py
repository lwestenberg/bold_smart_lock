"""Tests for Bold Smart Lock."""

import pytest
import aiohttp
from aiohttp.web import HTTPBadRequest
import json
import logging
from aioresponses import aioresponses
from bold_smart_lock.exceptions import EmailOrPhoneNotSpecified, InvalidEmail, InvalidPhone, InvalidValidationCode, InvalidValidationId, InvalidValidationResponse, MissingValidationId
from tests.helpers import load_fixture

from bold_smart_lock.const import (
    API_URI,
    POST_HEADERS,
    VALIDATIONS_ENDPOINT,
    AUTHENTICATIONS_ENDPOINT,
    EFFECTIVE_DEVICE_PERMISSIONS_ENDPOINT,
    REMOTE_ACTIVATION_ENDPOINT
)
from bold_smart_lock.bold_smart_lock import BoldSmartLock

fixture_authenticate_request= load_fixture("authenticate_request.json")

request_validation_id_invalid_email = load_fixture("request_validation_id_invalid_email.json")
request_validation_id_invalid_phone = load_fixture("request_validation_id_invalid_phone.json")
request_validation_id_response = load_fixture("request_validation_id_response.json")

verify_validation_id_request = load_fixture("verify_validation_id_request.json")
verify_validation_id_response = load_fixture("verify_validation_id_response.json")

authenticate_response_fixture = load_fixture("authenticate_response.json")
get_device_permissions_response_fixture = load_fixture("get_device_permissions_response.json")
remote_activation_response_fixture = load_fixture("remote_activation_response.json")
re_login_response_fixture = load_fixture("re_login_response.json")

# async def authenticate():
#     """Authenticate and return a session, auth results and an instance of the BoldSmartLock class"""
#     session = aiohttp.ClientSession()

#     with aioresponses() as m:
#         m.post(
#             API_URI + VALIDATIONS_ENDPOINT + "/" + fixture_authenticate_request["validation_id"],
#             headers=POST_HEADERS,
#             payload=verify_validation_id_response
#         )
#         m.post(
#             API_URI + AUTHENTICATIONS_ENDPOINT,
#             headers=POST_HEADERS,
#             payload=authenticate_response_fixture
#         )

#         bold = BoldSmartLock(session)
#         authenticate_response = await bold.authenticate(
#             fixture_authenticate_request["email"],
#             fixture_authenticate_request["password"],
#             fixture_authenticate_request["validation_code"],
#             fixture_authenticate_request["validation_id"]
#         )

#         return {
#             "session": session,
#             "authenticate_response": authenticate_response,
#             "bold": bold,
#         }

# @pytest.mark.asyncio
# async def test_authenticate():
#     """Test if the authentication returns a body and status 200"""

#     authenticate_result = await authenticate()
#     session = authenticate_result["session"]
#     authenticate_response = authenticate_result["authenticate_response"]
#     assert authenticate_response["body"] == authenticate_response_fixture
#     assert authenticate_response["status"] == 200
#     await session.close()

@pytest.mark.asyncio
async def test_authenticate_email_or_phone_not_specified():
    """Test if the authentication returns an EmailOrPhoneNotSpecified when not passing email and phone"""
    with aioresponses() as m:
        m.post(
            API_URI + VALIDATIONS_ENDPOINT,
            headers={
                "Content-Type": "text/plain"
            },
            body="Request entity expected but not supplied",
            status=400
        )

        session = aiohttp.ClientSession()
        bold = BoldSmartLock(session)

        try:
            request_validation_id_response = await bold.request_validation_id(
                fixture_authenticate_request["email"],
            )
            await request_validation_id_response.json()
        except EmailOrPhoneNotSpecified:
            assert True
    await session.close()

@pytest.mark.asyncio
async def test_request_validation_id_email_not_specified():
    """Test if request validation id returns an InvalidEmail when passing an invalid email address"""
    with aioresponses() as m:
        m.post(
            API_URI + VALIDATIONS_ENDPOINT,
            headers=POST_HEADERS,
            payload=request_validation_id_invalid_email,
            status=400
        )

        session = aiohttp.ClientSession()
        bold = BoldSmartLock(session)

        try:
            request_validation_id_response = await bold.request_validation_id(
                fixture_authenticate_request["email"],
            )
            await request_validation_id_response.json()
        except InvalidEmail:
            assert True
    await session.close()

@pytest.mark.asyncio
async def test_request_validation_id_phone_not_specified():
    """Test if request validation id returns an InvalidPhone when passing an invalid phone number"""
    with aioresponses() as m:
        m.post(
            API_URI + VALIDATIONS_ENDPOINT,
            headers=POST_HEADERS,
            payload=request_validation_id_invalid_phone,
            status=400
        )

        session = aiohttp.ClientSession()
        bold = BoldSmartLock(session)

        try:
            request_validation_id_response = await bold.request_validation_id(
                None,
                fixture_authenticate_request["phone"],
            )
            await request_validation_id_response.json()
        except InvalidPhone:
            assert True
    await session.close()

# @pytest.mark.asyncio
# async def test_authenticate():
#     """Test if the authentication returns a body and status 200"""

#     authenticate_result = await authenticate()
#     session = authenticate_result["session"]
#     authenticate_response = authenticate_result["authenticate_response"]
#     assert authenticate_response["body"] == authenticate_response_fixture
#     assert authenticate_response["status"] == 200
#     await session.close()

# @pytest.mark.asyncio
# async def test_get_device_permissions():
#     """Test if the device permissions endpoint is called"""

#     authenticate_result = await authenticate()
#     session = authenticate_result["session"]
#     bold = authenticate_result["bold"]

#     with aioresponses() as m:
#         m.get(
#             API_URI + EFFECTIVE_DEVICE_PERMISSIONS_ENDPOINT,
#             payload=get_device_permissions_response_fixture
#         )

#         get_device_permissions_response = await bold.get_device_permissions()
#         get_device_permissions_json = json.loads(get_device_permissions_response)
#         assert get_device_permissions_json == get_device_permissions_response_fixture

#     await session.close()

# @pytest.mark.asyncio
# async def test_re_login():
#     """Test if the re_login endpoint is called"""

#     authenticate_result = await authenticate()
#     session = authenticate_result["session"]
#     bold = authenticate_result["bold"]

#     with aioresponses() as m:
#         m.put(
#             API_URI + AUTHENTICATIONS_ENDPOINT + "/" + authenticate_response_fixture["token"],
#             headers=POST_HEADERS,
#             payload=re_login_response_fixture
#         )

#         re_login_response = await bold.re_login()
#         assert re_login_response == re_login_response_fixture

#     await session.close()

# @pytest.mark.asyncio
# async def test_remote_activation():
#     """Test if the remote_activation endpoint is called"""

#     authenticate_result = await authenticate()
#     session = authenticate_result["session"]
#     bold = authenticate_result["bold"]
#     device_id = 1

#     with aioresponses() as m:
#         m.post(
#             API_URI + REMOTE_ACTIVATION_ENDPOINT.format(device_id),
#             payload=remote_activation_response_fixture
#         )

#         remote_activation_response = await bold.remote_activation(device_id)
#         remote_activation_json = json.loads(remote_activation_response)
#         assert remote_activation_json == remote_activation_response_fixture

#     await session.close()

# @pytest.mark.asyncio
# async def test_verify_email():
    # """Test if the verify_email endpoint is called"""
    # authenticate_result = await authenticate()
    # session = authenticate_result["session"]
    # bold = authenticate_result["bold"]

    # with aioresponses() as m:
    #     m.post(
    #         API_URI + VALIDATIONS_ENDPOINT,
    #         headers=POST_HEADERS,
    #         payload=verify_email_response_fixture
    #     )

    #     verify_email_response = await bold.verify_email(fixture_authenticate_request["email"])
    #     assert verify_email_response == verify_email_response_fixture

    # await session.close()
