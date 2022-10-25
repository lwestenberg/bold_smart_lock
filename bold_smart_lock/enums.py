"""Enums used in the library Bold Smart Lock API library."""

from enum import Enum

class DeviceType(Enum):
    """All possible device types."""
    LOCK = 1
    GATEWAY = 2
    KEYFOB = 3
