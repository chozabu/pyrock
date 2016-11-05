"""Foobar.py: Description of what foobar does."""

__author__ = "Alex 'Chozabu' P-B"
__copyright__ = "Copyright 2016, Chozabu"

from transports import basic_tcp_json
import settings
import json

callbacks = {}

def send_packet(HOST, PORT, data, meta):
    meta['pkey'] = settings.pkey
    packet = json.dumps({"data":data, "meta":meta})
    ret = basic_tcp_json.send_data(HOST,PORT, packet)
    return ret

def on_recv_packet(data, sender):
    meta = data['meta']
    type = meta['type']
    if type in callbacks:
        for c in callbacks[type]:
            c(data, sender, meta)

def init(serve_port, send_port):
    basic_tcp_json.init(serve_port=serve_port, send_port=send_port)
    basic_tcp_json.on_recv_data = on_recv_packet

def hook_type(type, callback):
    if type not in callbacks:
        callbacks[type] = []
    callbacks[type].append(callback)