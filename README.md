# Bold Smart Lock Python Package

This package implements the Bold Smart Lock API to authenticate and unlock a Bold smart lock. Usage of this API requires a Bold Connect.

## Installation

## Usage

```python
import asyncio
import aiohttp
from datetime import datetime

from bold_smart_lock.bold_smart_lock import BoldSmartLock

async def main():
    async with aiohttp.ClientSession() as session:
        bold = BoldSmartLock(session)
        # Request a validation code for the account e-mail address
        verify_email_response = await bold.verify_email("john.doe@email.com);
        print(verify_email_response)

        # Authenticate with email, password, validation code (from email) and validation id (from output)
        authenticate_response = await bold.authenticate("john.doe@email.com", "password", "01234", "00000000-0000-0000-0000-000000000000");

        # E.g. for testing purpose you can set a token and expiration date manually
        token = "00000000-0000-0000-0000-000000000000"
        token_expiration_time = "2022-01-01T00:00:00.000000Z"
        bold.set_token_data(token, datetime.fromisoformat(token_expiration_time[:-1]))

        # Get the devices and device permissions
        get_device_permissions_response = await bold.get_device_permissions()
        print(get_device_permissions_response)

        # Active the smart lock by device id
        remote_activation_response = await bold.remote_activation(12345)
        print(remote_activation_response)

asyncio.run(main())
```
