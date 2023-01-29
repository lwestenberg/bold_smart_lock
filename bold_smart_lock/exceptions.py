"""Exceptions used in the library Bold Smart Lock API library."""

class ActivationError(Exception):
    """ActivationError exception for Bold."""

class DeactivationError(Exception):
    """DeactivationError exception for Bold."""

class GateWayCurrentSatatusError(Exception):
    """GateWayCurrentSatatusError exception for Bold."""

class DeviceFirmwareOutdatedError(Exception):
    """DeviceFirmwareOutdatedError exception for Bold."""

class TooManyRequestsError(Exception):
    """TooManyRequestsError exception for Bold."""

class GatewayUnreachableError(Exception):
    """GatewayUnreachableError exception for Bold."""

class GatewayNotFoundError(Exception):
    """GatewayNotFoundError exception for Bold."""
