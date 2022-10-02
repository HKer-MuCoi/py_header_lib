#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta

import sqlalchemy


class InterfaceEnum(sqlalchemy.types.TypeDecorator):
    __metaclass__ = ABCMeta
    cache_ok = False

    def __init__(self, enum_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enum_type

    def process_bind_param(self, value, dialect):
        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)


class IntEnum(InterfaceEnum):
    impl = sqlalchemy.types.Integer


class StringEnum(InterfaceEnum):
    impl = sqlalchemy.types.String
