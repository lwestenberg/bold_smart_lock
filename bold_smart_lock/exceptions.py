class AuthenticateFailed(Exception):
    """AuthenticateFailed exception for Bold."""

class InvalidEmail(Exception):
    """InvalidEmail exception for Bold."""

class InvalidPhone(Exception):
    """InvalidPhone exception for Bold."""

class EmailOrPhoneNotSpecified(Exception):
    """EmailOrPhoneNotSpecified exception for Bold."""

class EmailOrPhoneNotSpecified(Exception):
    """EmailOrPhoneNotSpecified exception for Bold."""

class MissingValidationId(Exception):
    """MissingValidationId exception for Bold."""

class InvalidValidationId(Exception):
    """InvalidValidationId exception for Bold."""

class InvalidValidationCode(Exception):
    """InvalidValidationCode exception for Bold."""

class InvalidValidationResponse(Exception):
    """InvalidValidationResponse exception for Bold."""

class VerificationNotFound(Exception):
    """VerificationNotFound exception for Bold."""

class Forbidden(Exception):
    """Forbidden exception for Bold."""

class TokenMissing(Exception):
    """TokenMissing exception for Bold."""

# verkeerd emailadres: 400, "errorMessage": "Invalid email address", "errorCode": "invalidEmailError"

# verkeerd of geen validationId = 405 not allowed, geen body
# verkeerde validationCode = 200, isVerified=falsde, numberOfAttempts telt op tot 3x daarna:
# 403, forbidden, body met errorMessage, geen errorCode

# Bij geldige validatie = "isVerified": true,
# in validatie home assistant:
# isExpired
# registrationRequired

# bij ongeldige auth: 401, met errorMessage, geen errorCode
# bij auth zonder login: 401 zonder errrorMessage

# expiration van validatie = 1 uur
# expiration van auth/sessie = 1 dag

# ongelgide relogin: 400, bad req, errorMessage, errorCode: UUIDMalformed maar bij ongeldige validationId geen code
# relogin zonder token: 405, not allowed

# device_permissions ongeldig token: 400, errorCode: UUIDMalformed, errorMessage

# token verlopen = 401
