#!/usr/bin/env python
# -*- coding: utf-8 -*-
import enum
from abc import ABCMeta


class EnumInterface(enum.Enum):
    __metaclass__ = ABCMeta

    # magic methods for argparse compatibility

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return str(self)

    @classmethod
    def argparse(cls, s):
        try:
            return cls[s.upper()]
        except KeyError:
            return s

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class UrBoxStatus(EnumInterface):
    Nothing = None
    DEACTIVATE = 1
    ACTIVATE = 2


class ReconciliationProcess(EnumInterface):
    NOTHING = None
    TEMPORARY = 0
    TRACKING = 11
    PENDING = 1
    PROCESSING = 2
    RESOLVED = 3
    GETTING_ERROR_REASON = 4
    DONE_GET_ERROR_REASON = 5
    DATA_ACCEPTED = 6
    DONE = 7


class EmailProcess(EnumInterface):
    NOTHING = None
    PENDING = 1
    SENT = 2
    DONE = 3


class PayProcess(EnumInterface):
    NOTHING = None
    NOT_PAID = 1
    PAID = 2


class ReconciliationType(EnumInterface):
    NOTHING = 0
    PRIMARY = 1
    SECONDARY = 2
    TRACKING = 3


class ReconciliationConfigType(EnumInterface):
    NOTHING = None
    DAY = 1
    MONTH = 2
    DAYS_OF_MONTH = 3
    DAYS_OF_WEEK = 4


class ReconciliationProcessCrossCheck(EnumInterface):
    NOTHING = None
    UPDATING_PENDING = 11
    UPDATING_PROCESSING = 12
    UPDATING_DONE = 13
    PAYING_PENDING = 21
    PAYING_PROCESSING = 22
    PAYING_DONE = 23


class DiscountType(EnumInterface):
    NOTHING = None
    PRODUCT = 1
    REVENUE = 2
    CONSTANT = 3


class ProcessType(EnumInterface):
    NOTHING = None
    PENDING = 1
    PROCESSING = 2
    DONE = 3


class ReconciliationCompareType(EnumInterface):
    NOTHING = None
    PENDING = 1
    MISMATCHED = 2
    MATCHED = 3
    MISMATCHED_MANUAL = 22
    MATCHED_MANUAL = 32
