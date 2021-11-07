"""Constants."""

# API endpoints
API_URI = "https://api.sesamtechnology.com/v1/"
VALIDATIONS_ENDPOINT = "validations"
AUTHENTICATIONS_ENDPOINT = "authentications"
REMOTE_ACTIVATION_ENDPOINT = "devices/{}/remote-activation"
EFFECTIVE_DEVICE_PERMISSIONS_ENDPOINT = "effective-device-permissions"

# Default headers
POST_HEADERS = {
    "Content-Type" : "application/json"
}

# Default JSON request data
AUTHENTICATION_REQUEST_JSON = {
    "clientType": "Android",
    "clientId": "234567890abcdef1",
    "clientDescription": "Samsung - Galaxy S",
    "clientVersion": "1.0",
    "appId": "sesam.technology.bold",
    "appDescription": "Bold Smart Lock - Android application",
    "appVersion": "1.8.1",
    "appName": "Bold Smart Lock",
    "notificationToken": "",
    "language": "en",
    "clientLocale": "en-US"
}
