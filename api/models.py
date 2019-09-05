import typing
from dataclasses import dataclass
from datetime import datetime

from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError

from .db import get_db


@dataclass
class Event:
    timestamp: datetime
    source_ip: str
    name: str
    extra_data: typing.Dict

    def __post_init__(self):
        self.timestamp = datetime.fromtimestamp(self.timestamp)

    def for_db(self):
        # Example format
        # {
        #     "measurement": "cpu_load_short",
        #     "tags": {
        #         "host": "server01",
        #         "region": "us-west"
        #     },
        #     "time": "2009-11-10T23:00:00Z",
        #     "fields": {
        #         "Float_value": 0.64,
        #         "Int_value": 3,
        #         "String_value": "Text",
        #         "Bool_value": True
        #     }
        # }
        return {
            "measurement": self.name,
            "time": self.timestamp.isoformat(),
            "fields": {
                **self.extra_data,
                "source_ip": self.source_ip
            },
            "tags": {
            }
        }

    def save(self):
        try:
            return get_db().write_points([self.for_db()])
        except (InfluxDBClientError, InfluxDBServerError) as exp:
            return False

    def get_self_from_db(self):
        query = f"select * from {self.name} where time = '{self.timestamp.isoformat()}Z'"
        result_set = get_db().query(query)
        if not result_set.error:
            for result in result_set.get_points(self.name):
                yield result
        return result_set.error

    @classmethod
    def query(cls, name, from_time=None, to=None, location=None):
        querystr = f"select * from {name} where"
        if from_time:
            querystr = f"{querystr} time >= '{from_time.isoformat()}Z'"
            if to or location:
                querystr = f"{querystr} and"
        if to:
            querystr = f"{querystr} time <= '{to.isoformat()}Z'"
            if location:
                querystr = f"{querystr} and"
        if location:
            querystr = f"{querystr} location = \"{location}\""
        print(querystr)
        result_set = get_db().query(querystr)
        if not result_set.error:
            for result in result_set.get_points(name):
                yield result
        return result_set.error
