"""Tests for Bold Smart Lock."""
import pytest
import aiohttp
import json
from aioresponses import aioresponses
from tests.helpers import load_fixture

from bold_smart_lock.const import (
    API_URI,
    EFFECTIVE_DEVICE_PERMISSIONS_ENDPOINT,
    REMOTE_ACTIVATION_ENDPOINT
)
from bold_smart_lock.bold_smart_lock import BoldSmartLock

fixture_authenticate_request= load_fixture("authenticate_request.json")
fixture_authenticate_response = load_fixture("authenticate_response.json")
fixture_get_device_permissions_response = load_fixture("get_device_permissions_response.json")
fixture_remote_activation_response = load_fixture("remote_activation_response.json")


@pytest.mark.asyncio
async def test_get_device_permissions():
    """Test if the device permissions endpoint is called"""
    session = aiohttp.ClientSession()
    bold = BoldSmartLock(session)
    bold.set_token(fixture_authenticate_response["token"])

    with aioresponses() as m:
        m.get(
            API_URI + EFFECTIVE_DEVICE_PERMISSIONS_ENDPOINT,
            payload=fixture_get_device_permissions_response
        )

        get_device_permissions_response = await bold.get_device_permissions()
        get_device_permissions_json = json.loads(get_device_permissions_response)
        assert get_device_permissions_json == fixture_get_device_permissions_response

    await session.close()

@pytest.mark.asyncio
async def test_remote_activation():
    """Test if the remote_activation endpoint is called"""
    session = aiohttp.ClientSession()
    bold = BoldSmartLock(session)
    bold.set_token(fixture_authenticate_response["token"])
    device_id = 1

    with aioresponses() as m:
        m.post(
            API_URI + REMOTE_ACTIVATION_ENDPOINT.format(device_id),
            payload=fixture_remote_activation_response
        )

        remote_activation_response = await bold.remote_activation(device_id)
        remote_activation_json = json.loads(remote_activation_response)
        assert remote_activation_json == fixture_remote_activation_response

    await session.close()
