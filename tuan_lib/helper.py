# -*- coding: utf-8 -*-
import datetime
import os
import time
import uuid
from base64 import b64encode

import requests
import pytz
from loguru import logger

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

from tuan_lib.http import FlaskRequestId

LOCAL_TIME_ZONE = "Asia/Bangkok"


class HttpRequest(object):
    SERVICE_ID = os.environ.get('SERVICE_ID') or 0

    @classmethod
    def is_success(cls, response):
        if response is not None and type(response) is dict \
                and 'success' in response and response.get('success') == True:
            return True
        return False

    @classmethod
    def __add_params(cls, params):
        if params is None:
            params = dict()
        current_unix_timestamp = int(time.time())
        uuid_note = uuid.uuid4().node
        query_params = params
        query_params.update(
            _sid=cls.SERVICE_ID,
            _aid=0,
            _rid=f'{current_unix_timestamp}{uuid_note}'
        )
        return query_params

    @classmethod
    def __add_headers(cls, headers=None):
        if headers is None:
            return {
                'X-Request-Id': FlaskRequestId.generate_request_id(),
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
            }
        else:
            headers.update(**{
                'X-Request-Id': FlaskRequestId.generate_request_id(),
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
            })
        return headers

    @classmethod
    def __content(cls, response):
        try:
            content = response.json()
        except Exception as e:
            logger.exception(e)
            content = response.content
        return content

    @classmethod
    def get(cls, url=None, params=None, headers=None):
        params = cls.__add_params(params)
        headers = cls.__add_headers(headers)
        content = None
        try:
            response = requests.get(url, params=params, headers=headers, auth=('urbox', 'urbox@170**'))

            if response.status_code == 200:
                content = cls.__content(response)
            else:
                logger.error("Call API {}: {}".format(url, response.content))
        except requests.ConnectionError as e:
            logger.exception(
                'OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.')
        except requests.Timeout as e:
            logger.exception('OOPS!! Timeout Error')
        except requests.RequestException as e:
            logger.exception('OOPS!! General Error')
        except Exception as e:
            logger.exception(e)
        return content

    @classmethod
    def post(cls, url=None, params=None, headers=None):
        params = cls.__add_params(params)
        headers = cls.__add_headers(headers)
        content = None
        try:
            response = requests.post(url, json=params, headers=headers, auth=('urbox', 'urbox@170**'))

            if response.status_code == 200:
                content = cls.__content(response)
            else:
                logger.error("Call API {}: {}".format(url, response.content))
        except requests.ConnectionError as e:
            logger.exception(
                'OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.')
        except requests.Timeout as e:
            logger.exception('OOPS!! Timeout Error')
        except requests.RequestException as e:
            logger.exception('OOPS!! General Error')
        except Exception as e:
            logger.exception(e)
        return content

    @classmethod
    def upload(cls, url, params=None, headers=None, files=None):
        params = cls.__add_params(params)
        headers = cls.__add_headers(headers)
        content = None
        try:
            response = requests.post(url, data=params, headers=headers, files=files, auth=('urbox', 'urbox@170**'))

            if response.status_code == 200:
                content = cls.__content(response)
            else:
                logger.error("Call API {}: {}".format(url, response.content))
        except requests.ConnectionError as e:
            logger.exception(
                'OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.')
        except requests.Timeout as e:
            logger.exception('OOPS!! Timeout Error')
        except requests.RequestException as e:
            logger.exception('OOPS!! General Error')
        except Exception as e:
            logger.exception(e)
        return content

    @classmethod
    def put(cls, url, params=None, headers=None):
        params = cls.__add_params(params)
        headers = cls.__add_headers(headers)
        content = None
        try:
            response = requests.put(url, json=params, headers=headers, auth=('urbox', 'urbox@170**'))

            if response.status_code == 200:
                content = cls.__content(response)
            else:
                logger.error("Call API {}: {}".format(url, response.content))
        except requests.ConnectionError as e:
            logger.exception(
                'OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.')
        except requests.Timeout as e:
            logger.exception('OOPS!! Timeout Error')
        except requests.RequestException as e:
            logger.exception('OOPS!! General Error')
        except Exception as e:
            logger.exception(e)
        return content


class Helper(object):
    @classmethod
    def get_now_unix_timestamp(cls):
        return int(time.time())

    @classmethod
    def get_now_datetime(cls, format_date='%Y-%m-%d %H:%M:%S'):
        now = datetime.datetime.now()
        return now.strftime(format_date)

    @classmethod
    def create_request_id(cls, prefix="UB"):
        time_code = datetime.datetime.now(pytz.timezone(LOCAL_TIME_ZONE)).strftime('%Y%m%d')
        request_code = uuid.uuid4().node
        return prefix + time_code + str(request_code)

    @classmethod
    def sha256_private_key_encode(cls, message, private_key):
        key = RSA.import_key(private_key)
        h = SHA256.new(message.encode())
        signature = pkcs1_15.new(key).sign(h)
        return b64encode(signature).decode("utf-8")
