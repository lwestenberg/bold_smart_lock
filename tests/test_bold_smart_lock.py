"""Tests for Bold Smart Lock."""
import pytest
import aiohttp
import json
from aioresponses import aioresponses
from tests.helpers import load_fixture

from bold_smart_lock.const import (
    API_URI,
    EFFECTIVE_DEVICE_PERMISSIONS_ENDPOINT,
    POST_HEADERS,
    REMOTE_ACTIVATION_ENDPOINT
)
from bold_smart_lock.bold_smart_lock import BoldSmartLock

fixture_authenticate_request= load_fixture("authenticate_request.json")
fixture_authenticate_response = load_fixture("authenticate_response.json")
fixture_get_device_permissions_response = load_fixture("get_device_permissions_response.json")
fixture_get_device_permissions_invalid_response = load_fixture("get_device_permissions_invalid_response.json")
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
        assert get_device_permissions_response == fixture_get_device_permissions_response

    await session.close()

@pytest.mark.asyncio
async def test_get_device_permissions_exceptions():
    """Test if get_device_permissions returns exceptions"""
    session = aiohttp.ClientSession()
    bold = BoldSmartLock(session)
    bold.set_token(fixture_authenticate_response["token"])

    with aioresponses() as m:
        m.get(
            API_URI + EFFECTIVE_DEVICE_PERMISSIONS_ENDPOINT,
            headers=POST_HEADERS,
            payload=fixture_get_device_permissions_invalid_response,
            status=401
        )

        try:
            await bold.get_device_permissions()
        except aiohttp.ClientError:
            assert True
        finally:
            await session.close()

@pytest.mark.asyncio
async def test_remote_activation():
    """Test if the remote_activation endpoint is called"""
    session = aiohttp.ClientSession()
    bold = BoldSmartLock(session)
    bold.set_token(fixture_authenticate_response["token"])

    with aioresponses() as m:
        m.post(
            API_URI + REMOTE_ACTIVATION_ENDPOINT.format(1),
            payload=fixture_remote_activation_response
        )

        remote_activation_response = await bold.remote_activation(1)
        assert remote_activation_response == fixture_remote_activation_response
        await session.close()

@pytest.mark.asyncio
async def test_remote_activation_invalid():
    """Test if the remote_activation endpoint returns errors"""
    session = aiohttp.ClientSession()
    bold = BoldSmartLock(session)
    bold.set_token(fixture_authenticate_response["token"])

    with aioresponses() as m:
        m.post(
            API_URI + REMOTE_ACTIVATION_ENDPOINT.format(1),
            status=403
        )

        try:
            await bold.remote_activation(1)
        except aiohttp.ClientError:
            assert True
        finally:
            await session.close()
