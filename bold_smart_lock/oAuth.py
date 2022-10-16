from aiohttp import ClientSession

from bold_smart_lock.const import API_URI, OAUTH_SERVICE

async def token(session: ClientSession):
    # TODO: finish
    try:
        async with session.post(
            API_URI + OAUTH_SERVICE + "/token",
            json={
                "grant_type": "password",
                "client_id": "",
                "client_secret": "",
                "username": "",
                "password": "",
                "mfa_token": ""
            }
        ) as response:
            return await response.json()
    except Exception as exception:
        raise exception
