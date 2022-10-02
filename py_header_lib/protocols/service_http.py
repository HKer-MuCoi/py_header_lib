#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py_header_lib.protocols.http_request import HttpRequest


class ServiceHttpConfig:
    def __init__(self, path: str = '', method: str = None, params_url_configs: list = []):
        self.path = path
        self.method = method
        self.params_url_configs = params_url_configs


class ServiceHttpBase:
    HOST = None
    NAMESPACE = None
    CONFIG = {}
    VERSION = None
    IS_ADD_URL_QUERY = False

    def __init__(self):
        self.host = self.__class__.HOST
        self.config = self.__class__.CONFIG
        self.namespace = self.__class__.NAMESPACE
        self.version = self.__class__.VERSION
        self.is_add_url_query = self.__class__.IS_ADD_URL_QUERY

    def call(self, name, params, headers, files=None):
        service_config = self.config[name]
        return self.call_with_config(service_config, params, headers, files)

    def call_with_config(self, config, params, headers, files=None):
        url = self.get_url_with_config_and_params(config, params)
        query_params = self.parse_params_with_config(params, config)
        request = HttpRequest(url=url, params=query_params, headers=headers)
        if config.method == 'upload':
            response = getattr(request, config.method)(files)
        else:
            response = getattr(request, config.method)()
        return self.handle_response(response)

    def parse_params_with_config(self, params, config) -> dict:  # noqa
        if not params or type(params) is not dict:
            return params

        query_params = params.copy()
        for config in config.params_url_configs:
            del query_params[config]
        return query_params

    def get_url_with_config_and_params(self, config, params) -> str:
        url = f'{self.host}{self.version}/{self.namespace}{config.path}'

        if self.is_add_url_query:
            url = f'{url}?_rid=0&_aid=0&_sid=0'

        if not params or type(params) is not dict:
            return url

        for config in config.params_url_configs:
            url.replace(f':{config}', params.get(config))
        return url


    def handle_response(self, response):  # noqa
        if response['success'] is True:
            return response.get('data') or True
        return None
