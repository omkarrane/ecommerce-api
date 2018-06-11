from rest_framework_jwt.settings import api_settings
from django.utils.encoding import smart_text

def generateToken(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


def decodeToken(token):
    try:
        auth = token.split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()
        value = auth[1]
        if(smart_text(auth[0].lower()) == auth_header_prefix):
            jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
            obj = jwt_decode_handler(value)
            return obj
        else:
            return False
    except:
        return False