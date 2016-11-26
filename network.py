"""Foobar.py: Description of what foobar does."""

__author__ = "Alex 'Chozabu' P-B"
__copyright__ = "Copyright 2016, Chozabu"

from transports import basic_tcp_json
from transports import simple_http_json
import settings
import machine
import json

callbacks = {}

def send_packet(HOST, PORT, data, meta):
    meta['pkey'] = settings.pkey
    packet = json.dumps({"data":data, "meta":meta})
    ret = simple_http_json.send_data(HOST,PORT, packet)
    if not ret[0]:
        ret = basic_tcp_json.send_data(HOST,PORT, packet)
    #ret = simple_http_json.send_data(HOST,PORT, packet)
    return ret

def on_recv_packet(data, sender):
    meta = data['meta']
    type = meta['type']
    print(settings.machine_name, "got", type, str(data))
    if type in callbacks:
        for c in callbacks[type]:
            c(data, sender, meta)

def init(serve_port):
    basic_tcp_json.init(serve_port=serve_port)
    basic_tcp_json.on_recv_data = on_recv_packet

    simple_http_json.init(serve_port=serve_port+10)
    simple_http_json.on_recv_data = on_recv_packet

def hook_type(type, callback):
    if type not in callbacks:
        callbacks[type] = []
    callbacks[type].append(callback)
