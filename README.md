# Bold Smart Lock Python Package

This package implements the Bold Smart Lock API to authenticate and unlock a Bold smart lock. Usage of this API requires a Bold Connect.

## Installation

To install dependencies during development run `pip install .` from the project directory.

## Run tests
Run `pip install pytest pytest-asyncio` to install the dependencies for testing.
Run `python -m pytest --asyncio-mode=auto` from the project directory.

## Usage

```python
import asyncio
import aiohttp

from bold_smart_lock.bold_smart_lock import BoldSmartLock

async def main():
  async with aiohttp.ClientSession() as session:
    bold = BoldSmartLock(session)

    # Request a validation id and validation code for the account e-mail address
    request_validation_id_response = await bold.request_validation_id("john.doe@email.com");
    print(request_validation_id_response)

    # Authenticate with email, password, validation code (from email) and validation id (from output)
    authenticate_response = await bold.authenticate("john.doe@email.com", "password", "01234", "00000000-0000-0000-0000-000000000000");
    print(authenticate_response)

    # E.g. for testing purpose you can set a token
    token = "00000000-0000-0000-0000-000000000000"
    bold.set_token(token)

    # Get the devices and device permissions
    get_device_permissions_response = await bold.get_device_permissions()
    print(get_device_permissions_response)

    # Active the smart lock by device id
    remote_activation_response = await bold.remote_activation(12345)
    print(remote_activation_response)

    # Re-login / update token
    relogin_response = await bold.re_login()
    print(relogin_response)

asyncio.run(main())
```
