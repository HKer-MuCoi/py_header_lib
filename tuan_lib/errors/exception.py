#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .const import HTTPStatusCode


class UrBoxException(Exception):
    status_code = HTTPStatusCode.SERVER_ERROR_INTERNAL_SERVER_ERROR
    message = 'Internal Server Error'

    def __init__(self, code=None, message=None):
        self.code = code or self.__class__.status_code
        self.message = message or self.__class__.message

    @property
    def to_dict(self) -> dict:
        return {
            'error': {
                'message': self.message, 'code': self.code.value
            }
        }


class BadRequest(UrBoxException):
    status_code = HTTPStatusCode.CLIENT_ERROR_BAD_REQUEST
    message = 'Bad Request'


class NotFound(UrBoxException):
    status_code = HTTPStatusCode.CLIENT_ERROR_NOT_FOUND
    message = 'Not Found'


class MethodNotAllowed(UrBoxException):
    status_code = HTTPStatusCode.CLIENT_ERROR_METHOD_NOT_ALLOWED
    message = 'Method Not Allowed'


class UnSupportedMediaType(UrBoxException):
    status_code = HTTPStatusCode.CLIENT_ERROR_UNSUPPORTED_MEDIA_TYPE
    message = 'Unsupported Media Type'


class Unauthorized(UrBoxException):
    status_code = HTTPStatusCode.CLIENT_ERROR_UNAUTHORIZED
    message = 'Unauthorized'


class RequestTimeOut(UrBoxException):
    status_code = HTTPStatusCode.CLIENT_ERROR_REQUEST_TIME_OUT
    message = 'Request Time Out'


class Forbidden(UrBoxException):
    status_code = HTTPStatusCode.CLIENT_ERROR_FORBIDDEN
    message = 'Forbidden'


class ExceptionFailed(UrBoxException):
    status_code = HTTPStatusCode.CLIENT_ERROR_EXPECTATION_FAILED
    message = 'Exception Failed'
