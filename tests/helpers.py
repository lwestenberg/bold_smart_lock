"""Helper methods for Bold Smart Lock tests."""
import os
import json


def load_fixture(filename, raw = False):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path) as fdp:
        return fdp.read() if raw else json.loads(fdp.read())
