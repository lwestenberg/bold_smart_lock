# Bold Smart Lock Python Package
This package implements the Bold Smart Lock API to authenticate and unlock a Bold smart lock. Usage of this API requires a Bold Connect.

## Installation
To install dependencies during development run ```pip install .``` from the project directory.
Optionally use the included VSCode Dev Container to get a preconfigured envirionment.

## Usage

```python
import asyncio
import aiohttp
from bold_smart_lock.auth import AbstractAuth

from bold_smart_lock.bold_smart_lock import BoldSmartLock

class TestAuth(AbstractAuth):
    async def async_get_access_token(self) -> str:
        return "00000000-0000-0000-0000-000000000000"  # Obtain an access token with oAuth2 and specify it here

async def main():
  async with aiohttp.ClientSession() as session:
    auth = TestAuth(session)
    bold = BoldSmartLock(auth)

    # Get the devices and device permissions
    get_device_permissions_response = await bold.get_device_permissions()
    print(get_device_permissions_response)

    # Activate the smart lock by device id
    remote_activation_response = await bold.remote_activation(12345)
    print(remote_activation_response)

    # Deactivate the smart lock by device id
    remote_deactivation_response = await bold.remote_deactivation(12345)
    print(remote_deactivation_response)

asyncio.run(main())
```
