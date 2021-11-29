#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import time

from loguru import logger


class Moment:
    def __init__(self, unix_timestamp: int = None, format_time: str = None):
        self.unix_timestamp = unix_timestamp or int(time.time())
        self.format_time = format_time or '%Y-%m-%d %H:%M:%S'

    @classmethod
    def from_datetime(cls, datetime_value: str, format_time: str):
        try:
            unix_timestamp = int(time.mktime(datetime.datetime.strptime(datetime_value, format_time).timetuple()))
        except Exception as e:
            logger.exception(e)
            unix_timestamp = 0

        return Moment(unix_timestamp, format_time)

    def to_unix_timestamp(self):
        return self.unix_timestamp

    def to_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.unix_timestamp)

    def to_string(self) -> str:
        return datetime.datetime.utcfromtimestamp(self.unix_timestamp).strftime(self.format_time)

    def add_days(self, days: int):
        datetime_value = datetime.datetime.fromtimestamp(self.unix_timestamp)
        time_delta = datetime_value + datetime.timedelta(days=days)
        time_delta = time_delta.replace(minute=59, hour=23, second=59)
        self.unix_timestamp = int(time_delta.strftime('%s'))
        return self
