"""Effective device permissions API V1"""
from aiohttp import ClientSession

from bold_smart_lock.const import API_URI, EFFECTIVE_DEVICE_PERMISSIONS_SERVICE


async def get_device_permissions(session: ClientSession):
    """Get all effective device permissions"""

    # TODO: add auth

    try:
        async with session.get(
            API_URI + EFFECTIVE_DEVICE_PERMISSIONS_SERVICE
        ) as response:
            return await response.json()
    except Exception as exception:
        raise exception
