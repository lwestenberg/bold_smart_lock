"""Library to access the Bold Smart Lock API."""

from __future__ import annotations

from .auth import AbstractAuth
from .const import (
    API_URL,
    DEVICE_SERVICE,
    GATEWAY_SERVICE,
    EFFECTIVE_DEVICE_PERMISSIONS_SERVICE,
)
from .exceptions import (
    ActivationError,
    DeactivationError,
    DeviceFirmwareOutdatedError,
    GateWayCurrentSatatusError,
    GatewayNotFoundError,
    TooManyRequestsError,
    GatewayUnreachableError,
)


class BoldSmartLock:
    """Class to communicate with the Bold Smart Lock API."""

    def __init__(self, auth: AbstractAuth):
        self._auth = auth

    async def get_device_permissions(self):
        """Get all effective device permissions."""
        try:
            response = await self._auth.request(
                "GET", f"{API_URL}{EFFECTIVE_DEVICE_PERMISSIONS_SERVICE}"
            )
            response_json = await response.json()
            return response_json
        except Exception as exception:
            raise exception

    async def remote_activation(self, device_id: int):
        """Remotely activate a device, using a gateway."""
        try:
            response = await self._auth.request(
                "POST", f"{API_URL}{DEVICE_SERVICE}/{device_id}/remote-activation"
            )
            response_json = await response.json()

            if response_json["errorCode"] == "TooManyRequests":
                raise TooManyRequestsError
            if response_json["errorCode"] == "gatewayNotFoundError":
                raise GatewayNotFoundError
            if response_json["errorCode"] != "OK":
                raise ActivationError

            return response_json
        except Exception as exception:
            raise exception

    async def remote_deactivation(self, device_id: int):
        """Remotely deactivate a device, using a gateway."""
        try:
            response = await self._auth.request(
                "POST", f"{API_URL}{DEVICE_SERVICE}/{device_id}/remote-deactivation"
            )
            response_json = await response.json()

            if response_json["errorCode"] == "TooManyRequests":
                raise TooManyRequestsError
            if response_json["errorCode"] == "DeviceFirmwareOutdated":
                raise DeviceFirmwareOutdatedError
            if response_json["errorCode"] == "gatewayNotFoundError":
                raise GatewayNotFoundError
            elif response_json["errorCode"] != "OK":
                raise DeactivationError

            return response_json
        except Exception as exception:
            raise exception

    async def gateway_current_status(self, gateway_id: int):
        """Retrieve curren status of a gateway."""
        try:
            response = await self._auth.request(
                "GET", f"{API_URL}{GATEWAY_SERVICE}/{gateway_id}/current-status"
            )
            response_json = await response.json()

            if response_json["errorCode"] == "TooManyRequests":
                raise TooManyRequestsError
            if response_json["errorCode"] == "GatewayUnreachable":
                raise GatewayUnreachableError
            elif response_json["errorCode"] != "OK":
                raise GateWayCurrentSatatusError

            return response_json
        except Exception as exception:
            raise exception
