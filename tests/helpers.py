"""Helper methods for Bold Smart Lock tests."""
from __future__ import annotations
from aioresponses import aioresponses
from bold_smart_lock.auth import Auth
from bold_smart_lock.const import API_URI, AUTHENTICATIONS_ENDPOINT, POST_HEADERS, VALIDATIONS_ENDPOINT

import aiohttp
import json
import os


def load_fixture(filename: str, raw: bool = False):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path) as fdp:
        return fdp.read() if raw else json.loads(fdp.read())

fixture_authenticate_request: dict[str, str] = load_fixture("authenticate_request.json")
fixture_request_validation_id_response: dict[str, str] = load_fixture("request_validation_id_response.json")
fixture_verify_validation_id_response: dict[str, str] = load_fixture("verify_validation_id_response.json")
fixture_authenticate_response: dict[str, str] = load_fixture("authenticate_response.json")

async def mock_auth_authenticate(
    mock_request_validation_id_response: list = None,
    mock_fixture_verify_validation_id_response: list = None,
    mock_authenticate_reponse: list = None,
    mock_auth: Auth = None,
    mock_session: aiohttp.ClientSession = None
) -> dict[str, str]:
    """Helper to set mocking for request+verify validation id and authenticate calls"""
    with aioresponses() as m:
        if mock_request_validation_id_response:
            m.post(
                API_URI + VALIDATIONS_ENDPOINT,
                headers=POST_HEADERS,
                status=mock_request_validation_id_response[0] or 200,
                payload=mock_request_validation_id_response[1] or fixture_request_validation_id_response,
            )
        if mock_fixture_verify_validation_id_response:
            m.post(
                API_URI + VALIDATIONS_ENDPOINT + "/" + fixture_request_validation_id_response["id"],
                headers=POST_HEADERS,
                status=mock_fixture_verify_validation_id_response[0] or 200,
                payload=mock_fixture_verify_validation_id_response[1] or fixture_verify_validation_id_response,
            )
        if mock_authenticate_reponse:
            m.post(
                API_URI + AUTHENTICATIONS_ENDPOINT,
                headers=POST_HEADERS,
                status=mock_authenticate_reponse[0] or 200,
                payload=mock_authenticate_reponse[1] or fixture_authenticate_response,
            )

        try:
            session = mock_session or aiohttp.ClientSession()
            auth = mock_auth or Auth(session)
            return await auth.authenticate(
                fixture_authenticate_request["email"],
                fixture_authenticate_request["password"],
                fixture_authenticate_request["validation_code"],
                fixture_authenticate_request["validation_id"]
            )
        except Exception as exception:
            raise exception
        finally:
            await session.close()

async def mock_auth_request_validation_id(
    status: int = 200,
    verification_method: str = "email",
    headers: str = "application/json",
    response: dict[str, str] = fixture_request_validation_id_response,
) -> dict[str, str]:
    """Helper to set mocking for request_validation_id calls"""
    with aioresponses() as m:
        m.post(
            API_URI + VALIDATIONS_ENDPOINT,
            headers=headers or POST_HEADERS,
            status=status,
            payload=response,
        )

        try:
            session = aiohttp.ClientSession()
            auth = Auth(session)
            return await auth.request_validation_id(
                fixture_authenticate_request["email"] if verification_method == "email" else fixture_authenticate_request["phone"],
            )
        except Exception as exception:
            raise exception
        finally:
            await session.close()
