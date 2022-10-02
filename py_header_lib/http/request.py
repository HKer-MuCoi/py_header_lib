# -*- coding: utf-8 -*-
"""
Middleware and logging filter to add request ids to logs and forward request ids in downstream requests
"""
from loguru import logger

import py_header_lib.http # noqa
import os
from flask import request, abort
import datetime
import uuid
import pytz
import time

REQUEST_ID_HEADER_NAME = os.environ.get('REQUEST_ID_HEADER') or 'X-Request-Id'
LOG_TOKENS = os.environ.get('LOG_TOKENS') or True
LOCAL_TIME_ZONE = 'Asia/Bangkok'


def make_header_key(header: str):
    wsgi_header = 'HTTP_' + header.replace('-', '_').upper()
    return wsgi_header


def make_request_id(first_request_id='REQ', time_zone=LOCAL_TIME_ZONE):
    middle_request_id = datetime.datetime.now(pytz.timezone(time_zone)).strftime('%Y%m%d')
    last_request_id = str(uuid.uuid4().node)
    return first_request_id + middle_request_id + last_request_id


def current_milliseconds_time():
    return round(time.time() * 1000)


def current_full_time():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%dT%H:%M:%S%z.%f')


class FlaskRequestId(object):

    @classmethod
    def generate_request_id(cls, first_request_id='REQ', time_zone=LOCAL_TIME_ZONE):
        middle_request_id = datetime.datetime.now(pytz.timezone(time_zone)).strftime('%Y%m%d')
        last_request_id = str(uuid.uuid4().node)
        return first_request_id + middle_request_id + last_request_id

    """
    This middleware add access log-style record with a request id and includes
    the request Id in int he response headers
    """

    def __init__(self, app=None, header_name: str = None):
        self.header_name = header_name
        if not self.header_name:
            self.header_name = REQUEST_ID_HEADER_NAME
        self.header_key = make_header_key(self.header_name)
        self.app = None
        self.start_time = 0
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app.wsgi_app
        app.before_request(self.before_request)
        app.wsgi_app = self

    def get_header_key(self):
        return self.header_key

    def get_header_name(self):
        return self.header_name

    def before_request(self):
        self.start_time = current_milliseconds_time()
        request_id = request.headers.get(self.header_name, None)
        if request_id is None:
            abort(404, description='Page not found')

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            # append whatever headers you need here
            request_id = environ.get(self.header_key, None)

            latency_time = current_milliseconds_time() - self.start_time
            message = {
                'client_id': environ.get('REMOTE_ADDR', ''),
                'latency_time': latency_time,
                'level': 'info',
                'msg': '',
                'req_method': environ.get('REQUEST_METHOD', ''),
                'req_uri': environ.get('PATH_INFO', ''),
                'status_code': int(status[:3]),
                'time': current_full_time(),
                'request_id': request_id,
            }

            # The response status code 404 when header not found request_id
            if request_id is None:
                print("Page not found")
                start_response("404 Not Found", [('Content-type', 'text/plain')])
                abort(404, description='Page not found')
                return

            # Write log to console
            logger.info(message)

            headers.append((self.header_name, request_id,))
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)
