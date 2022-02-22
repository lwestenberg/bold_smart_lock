"""Tests for Bold Smart Lock."""
from __future__ import annotations
from aiohttp.web import HTTPUnauthorized
from aioresponses import aioresponses
from bold_smart_lock.auth import Auth
from bold_smart_lock.const import API_URI, AUTHENTICATIONS_ENDPOINT, POST_HEADERS
from bold_smart_lock.exceptions import AuthenticateFailed, EmailOrPhoneNotSpecified, InvalidEmail, InvalidPhone, InvalidValidationCode, InvalidValidationId, InvalidValidationResponse, MissingValidationId, TokenMissing, VerificationNotFound

from tests.helpers import load_fixture, mock_auth_authenticate, mock_auth_request_validation_id

import aiohttp
import pytest

fixture_re_login_response: dict[str, str] = load_fixture("re_login_response.json")
fixture_request_validation_id_invalid_email: dict[str, str] = load_fixture("request_validation_id_invalid_email.json")
fixture_request_validation_id_invalid_phone: dict[str, str] = load_fixture("request_validation_id_invalid_phone.json")


@pytest.mark.asyncio
async def test_authenticate():
    """Test if a valid request returns the json payload and sets the token"""
    session = aiohttp.ClientSession()
    auth = Auth(session)
    initial_token = auth.token()
    auth_response = await mock_auth_authenticate([None, None], [None, None], [None, None], auth, session)
    verification_token = auth.token()
    assert initial_token is None and verification_token != initial_token and auth_response["token"] == verification_token

@pytest.mark.asyncio
async def test_authenticate_invalid():
    """Test if an invalid request returns an AuthenticateFailed error"""
    try:
        await mock_auth_authenticate([None, None], [None, None], [201, None])
    except AuthenticateFailed:
        assert True

@pytest.mark.asyncio
async def test_authenticate_invalid_body():
    """Test if a 401 error coming from an invalid post body or login results in a HTTPUnauthorized error"""
    try:
        await mock_auth_authenticate([None, None], [None, None], [401, None])
    except HTTPUnauthorized:
        assert True

@pytest.mark.asyncio
async def test_authenticate_invalid_body():
    """Test if a 404 error coming from an invalid validation id results in a VerificationNotFound error"""
    try:
        await mock_auth_authenticate([None, None], [None, None], [404, None])
    except VerificationNotFound:
        assert True

@pytest.mark.asyncio
async def test_headers_text_output():
    """Test if headers with output type text returns an empty object"""
    session = aiohttp.ClientSession()
    auth = Auth(session)
    headers = auth.headers(True)
    assert bool(headers) is False

@pytest.mark.asyncio
async def test_headers_json_output():
    """Test if headers with output type json returns POST headers"""
    session = aiohttp.ClientSession()
    auth = Auth(session)
    headers = auth.headers(False)
    assert headers == POST_HEADERS

@pytest.mark.asyncio
async def test_re_login():
    """Test if a succesful relogin returns data with a token"""
    token = "00000000-0000-0000-0000-000000000000"
    session = aiohttp.ClientSession()
    auth = Auth(session)
    auth.set_token(token)

    with aioresponses() as m:
        m.put(
            API_URI + AUTHENTICATIONS_ENDPOINT + "/" + token,
            headers=POST_HEADERS,
            status=200,
            payload=fixture_re_login_response
        )

        response: dict[str, str] = await auth.re_login()
        await session.close()
        assert response["token"] == "10000000-0000-0000-0000-001234567890"

@pytest.mark.asyncio
async def test_re_login_invalid():
    """Test if a relogin without token returns TokenMissing error"""
    session = aiohttp.ClientSession()
    auth = Auth(session)

    with aioresponses() as m:
        m.put(
            API_URI + AUTHENTICATIONS_ENDPOINT + "/",
            status=401,
        )
        try:
            await auth.re_login()
        except TokenMissing:
            assert True

@pytest.mark.asyncio
async def test_verify_validation_id_missing_validation_id():
    """Test if verify validation id returns an MissingValidationId error when no validation id was passed"""
    try:
        await mock_auth_authenticate([None, None], [405, None])
    except MissingValidationId:
        assert True

@pytest.mark.asyncio
async def test_verify_validation_id_invalid_validation_id():
    """Test if verify validation id returns an InvalidValidationId error when no validation id was passed"""
    try:
        await mock_auth_authenticate([None, None], [404, None])
    except InvalidValidationId:
        assert True

@pytest.mark.asyncio
async def test_verify_validation_id_missing_validation_code():
    """Test if verify validation id returns an MissingValidationCode error when no validation code was passed"""
    try:
        await mock_auth_authenticate([None, None], [400, None])
    except InvalidValidationCode:
        assert True

@pytest.mark.asyncio
async def test_verify_validation_id_invalid_response():
    """Test if verify validation id returns an InvalidValidationResponse error for uncatched response statusses"""
    try:
        await mock_auth_authenticate([None, None], [202, None])
    except InvalidValidationResponse:
        assert True

@pytest.mark.asyncio
async def test_request_validation_id_email_or_phone_not_specified():
    """Test if the authentication returns an EmailOrPhoneNotSpecified when not passing email and phone"""
    try:
        await mock_auth_request_validation_id(400, "email", {"Content-Type": "text/plain"})
    except EmailOrPhoneNotSpecified:
        assert True

@pytest.mark.asyncio
async def test_request_validation_id_phone_not_specified():
    """Test if the authentication returns an InvalidPhone when not passing a phone number"""
    try:
        await mock_auth_request_validation_id(400, "phone", None, fixture_request_validation_id_invalid_phone)
    except InvalidPhone:
        assert True

@pytest.mark.asyncio
async def test_request_validation_id_phone_not_specified():
    """Test if the authentication returns an InvalidEmail when not passing an email address"""
    try:
        await mock_auth_request_validation_id(400, "email", None, fixture_request_validation_id_invalid_email)
    except InvalidEmail:
        assert True
