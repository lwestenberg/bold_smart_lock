"""Bold Smart Lock API wrapper"""
from __future__ import annotations
from aiohttp import ClientSession

class BoldSmartLock:
    """A Python Abstraction object to Bold Smart Lock"""

    def __init__(self, session: ClientSession):
        """Initialize the Bold Smart Lock object."""
