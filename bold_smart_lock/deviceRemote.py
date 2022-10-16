"""Device Remote API V1"""

from aiohttp import ClientSession

from bold_smart_lock.const import API_URI, DEVICE_SERVICE
from bold_smart_lock.exceptions import MissingDeviceId


async def remote_activation(session: ClientSession, device_id: int):
    """This method allows you to remotely activate a device, using a gateway."""
    """The status of the server-call and the lock-activation are displayed differently."""
    """If the server returns a 200, that means that the server-call has succeeded. The result of the lock-activation is logged in the body of the return object."""

    # TODO: add auth

    if not device_id:
        raise MissingDeviceId
    else:
        try:
            async with session.post(
                API_URI + DEVICE_SERVICE + "/" + device_id + "/remote-activation",
            ) as response:
                return await response.json()
        except Exception as exception:
            raise exception
