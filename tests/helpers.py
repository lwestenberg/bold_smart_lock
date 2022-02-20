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
request_validation_id_invalid_email = load_fixture("request_validation_id_invalid_email.json")
request_validation_id_invalid_phone = load_fixture("request_validation_id_invalid_phone.json")
request_validation_id_response = load_fixture("request_validation_id_response.json")

verify_validation_id_request = load_fixture("verify_validation_id_request.json")
verify_validation_id_response = load_fixture("verify_validation_id_response.json")

authenticate_response_fixture = load_fixture("authenticate_response.json")
get_device_permissions_response_fixture = load_fixture("get_device_permissions_response.json")
remote_activation_response_fixture = load_fixture("remote_activation_response.json")

async def mock_auth_authenticate(
    mock_get_validation_id_response = None,
    mock_verify_validation_id_response = None,
    mock_authenticate_reponse = None,
    mock_auth = None,
    mock_session = None
):
    with aioresponses() as m:
        if mock_get_validation_id_response:
            m.post(
                API_URI + VALIDATIONS_ENDPOINT,
                headers=POST_HEADERS,
                status=mock_get_validation_id_response[0] or 200,
                payload=mock_get_validation_id_response[1] or request_validation_id_response,
            )
        if verify_validation_id_response:
            m.post(
                API_URI + VALIDATIONS_ENDPOINT + "/" + request_validation_id_response["id"],
                headers=POST_HEADERS,
                status=mock_verify_validation_id_response[0] or 200,
                payload=mock_verify_validation_id_response[1] or verify_validation_id_response,
            )
        if mock_authenticate_reponse:
            m.post(
                API_URI + AUTHENTICATIONS_ENDPOINT,
                headers=POST_HEADERS,
                status=mock_authenticate_reponse[0] or 200,
                payload=mock_authenticate_reponse[1] or authenticate_response_fixture,
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
