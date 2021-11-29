#!/usr/bin/env python
# -*- coding: utf-8 -*-
import grpc
from google.protobuf.json_format import MessageToDict
from loguru import logger


class ServiceGrpcConfig:
    def __init__(self, method: str = None, func_parse_input=None):
        self.method = method
        self.func_parse_input = func_parse_input


class ServiceGrpcBase:
    HOST = None
    CONFIG = None
    NAMESPACE = None

    def __init__(self):
        self.host = self.__class__.HOST
        self.config = self.__class__.CONFIG
        self.namespace = self.__class__.NAMESPACE

    def call(self, name, params, headers):
        method = self.config[name]
        return self.call_with_method(method, params)

    def call_with_method(self, config, params):
        channel = grpc.insecure_channel(self.host)
        stub = self.namespace(channel)
        query_params = config.func_parse_input(body=params)
        response = getattr(stub, config.method)(query_params)
        return self.handle_response(response)

    def handle_response(self, response):  # noqa
        if response.success is True:
            response = MessageToDict(response.data, preserving_proto_field_name=True, including_default_value_fields=True)
        else:
            response = None
        logger.info(f'RESPONSE: {response}')
        return response
