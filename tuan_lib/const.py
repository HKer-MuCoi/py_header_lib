import os
from enum import Enum

SUPPLIER_CONTACT_EMAIL = 3
URBOX_SECRET = os.environ.get('URBOX_SECRET') or "UrBox"


class Status(Enum):
    ON = 2
    OFF = 1
    NOTHING = None


class DISCOUNT(Enum):
    PRODUCT = 1
    REVENUE = 2
    CONSTANT = 3


class Protocol(Enum):
    GRPC = 'grpc'
    HTTP = 'http'


class HttpMethod(Enum):
    POST = 1
    PUT = 2
    GET = 3
