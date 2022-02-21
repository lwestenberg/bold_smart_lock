"""Helper methods for Bold Smart Lock tests."""
import os
import json
import aiohttp
from aioresponses import aioresponses
from bold_smart_lock.auth import Auth
from bold_smart_lock.const import API_URI, AUTHENTICATIONS_ENDPOINT, POST_HEADERS, VALIDATIONS_ENDPOINT


def load_fixture(filename, raw = False):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path) as fdp:
        return fdp.read() if raw else json.loads(fdp.read())

fixture_authenticate_request= load_fixture("authenticate_request.json")
fixture_request_validation_id_response = load_fixture("request_validation_id_response.json")
fixture_verify_validation_id_response = load_fixture("verify_validation_id_response.json")
fixture_authenticate_response = load_fixture("authenticate_response.json")

async def mock_auth_authenticate(
    mock_request_validation_id_response = None,
    mock_fixture_verify_validation_id_response = None,
    mock_authenticate_reponse = None,
    mock_auth = None,
    mock_session = None
):
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
    status = 200,
    verification_method = "email",
    headers = "application/json",
    response = fixture_request_validation_id_response,
):
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
