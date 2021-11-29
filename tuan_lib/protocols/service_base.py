#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ServiceBase:
    PROTOCOL_TYPE = 'grpc'
    PROTOCOL_GRPC = None
    PROTOCOL_HTTP = None

    def __init__(self, protocol_type=None):
        self.protocol_type = protocol_type or self.__class__.PROTOCOL_TYPE
        self.protocol_grpc = self.__class__.PROTOCOL_GRPC
        self.protocol_http = self.__class__.PROTOCOL_HTTP

    def set_protocol(self, protocol_type):
        self.protocol_type = protocol_type

    def call(self, name, params, headers, files=None):
        protocol_request = self.get_protocol_request()
        return protocol_request.call(name, params, headers, files=files)

    def get_protocol_request(self):
        selector = {
            'grpc': self.protocol_grpc,
            'http': self.protocol_http
        }

        return selector[self.protocol_type]
