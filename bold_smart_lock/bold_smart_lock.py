"""Library to access the Bold Smart Lock API"""

from __future__ import annotations

from .auth import AbstractAuth
from .const import API_URL, DEVICE_SERVICE

class Bold:
    """Class to communicate with the Bold Smart Lock API."""

    def __init__(self, auth: AbstractAuth):
        self._auth = auth

    async def remote_activation(self, device_id: int):
        """Remotely activate a device, using a gateway."""
        self._auth.request("POST", f"{API_URL}{DEVICE_SERVICE}/device/{device_id}/remote-activation")

    async def get_device_permissions(self):
        """Get all effective device permissions"""
        self._auth.request("GET", f"{API_URL}{DEVICE_SERVICE}/effective-device-permissions")
