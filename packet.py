"""Foobar.py: Description of what foobar does."""

__author__ = "Alex 'Chozabu' P-B"
__copyright__ = "Copyright 2016, Chozabu"

import json

class Packet:
    def __init__(self):
        pass
    def from_dicts(self, data, meta):
        self.data_string = json.dumps(data)
        self.meta_string = json.dumps(meta)
        self.data = data
        self.meta = meta
    def from_strings(self, data, meta):
        self.data = json.loads(data)
        self.meta = json.loads(meta)
        self.data_string = data
        self.meta_string = meta


data = {
    "anythinggoes": "in data",
    "title": "test"
}
meta = {
    "type": "synclistitem",
    "subtype": "?",
    "signature": "123",
    "hash": "456"
}