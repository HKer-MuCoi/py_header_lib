#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import uuid

import requests
from loguru import logger

from tuan_lib.errors.const import HTTPStatusCode
from tuan_lib.errors.exception import Forbidden, RequestTimeOut, ExceptionFailed
from tuan_lib.http import FlaskRequestId


class HttpRequest:
    SERVICE_ID = os.environ.get('SERVICE_ID') or 0

    def __init__(self, url=None, params=None, headers=None, auth: tuple = None, files=None):
        if headers is None:
            headers = {}

        self.url = url
        self.auth = auth or ('urbox', 'urbox@170**')
        self.params = params
        self.files = files
        self.content = None
        self.headers = headers
        self.__update_headers()


    def set_files(self, files):
        self.files = files

    def set_headers(self, headers=None):
        if headers is None:
            headers = {}

        self.headers = headers
        self.__update_headers()

    def __update_headers(self):
        self.headers.update(**{
            'x-request-id': FlaskRequestId.generate_request_id(),
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        })

    def get(self):
        if self.content:
            return self.content

        try:
            response = requests.get(self.url, params=self.params, headers=self.headers, auth=self.auth)
            self.__handle_response(response)
        except requests.ConnectionError as e:
            raise Forbidden()
        except requests.Timeout as e:
            raise RequestTimeOut()
        except requests.RequestException as e:
            raise ExceptionFailed()
        except Exception as e:
            logger.exception(e)
        return self.content

    def post(self):
        if self.content:
            return self.content

        try:
            response = requests.post(self.url, json=self.params, headers=self.headers, auth=self.auth)
            self.__handle_response(response)
        except requests.ConnectionError as e:
            raise Forbidden()
        except requests.Timeout as e:
            raise RequestTimeOut()
        except requests.RequestException as e:
            raise ExceptionFailed()
        except Exception as e:
            logger.exception(e)
        return self.content

    def upload(self, files=None):
        try:
            response = requests.post(self.url, data=self.params, headers=self.headers, files=self.files, auth=self.auth)
            self.__handle_response(response)
        except requests.ConnectionError as e:
            raise Forbidden()
        except requests.Timeout as e:
            raise RequestTimeOut()
        except requests.RequestException as e:
            raise ExceptionFailed()
        except Exception as e:
            logger.exception(e)
        return self.content

    def put(self):
        try:
            response = requests.put(self.url, json=self.params, headers=self.headers, auth=self.auth)
            self.__handle_response(response)
        except requests.ConnectionError as e:
            raise Forbidden()
        except requests.Timeout as e:
            raise RequestTimeOut()
        except requests.RequestException as e:
            raise ExceptionFailed()
        except Exception as e:
            logger.exception(e)
        return self.content

    def __handle_response(self, response):
        if HTTPStatusCode(response.status_code) == HTTPStatusCode.SUCCESS_OK:
            self.__handle_response_content(response)
        else:
            logger.error("Call API {}: {}".format(self.url, response.content))

    def __handle_response_content(self, response):
        try:
            self.content = response.json()
        except Exception as e:
            logger.exception(e)
            self.content = response.content
        logger.info(f'Response: {self.content}')
