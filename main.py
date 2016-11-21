"""Foobar.py: Description of what foobar does."""

__author__ = "Alex 'Chozabu' P-B"
__copyright__ = "Copyright 2016, Chozabu"

import defopt
import json

import html_ui
import websockets_ui
import machine
import network
import settings
import synclist
import time
from apps import basic_chat

import random

def test_cb(data, sender, meta):
    print(settings.machine_name, "MAINCB", data, sender, sender.ip, sender.name)

def main(settingsfile="settings.json", test_mode=False):
    """Display a friendly greeting.

    :param str settingsfile: settings file to load
    :param bool test_mode: True to run some tests
    """

    #load settings
    with open(settingsfile) as data_file:
        data = json.load(data_file)
        machinesfile = data['machines_file']
        settings.machine_name = data['machine_name']
        settings.pkey = data['pkey']
        settings.ui_port = data['ui_port']

    #init network
    network.init(data['serve_port'], data['send_port'])
    network.hook_type("hello", test_cb)

    #init synclist
    synclist.init()

    #init basic_chat
    basic_chat.init()

    #init html
    html_ui.init()
    websockets_ui.init()

    #load machines
    machine.loadcontacts(machinesfile)

    #connect to all?

    print("Init Complete")

    if test_mode:
        run_tests()

    while settings.running:
        time.sleep(1)


def run_tests():
    print("Running tests")
    test_sl = synclist.create_synclist("global_test")

    #get machine for testing
    tf = machine.machines[0]
    #print(settings.machine_name, tf)

    #sleep, send test packet, then sleep again
    time.sleep(.2)
    #ret = tf.send_data("test")
    ret = tf.send_packet({}, {"type":"hello"})
    print(settings.machine_name, ret)
    time.sleep(.2)#+random.random())

    test_sl.publish_item({"testitem":"I am "+ settings.machine_name})

    time.sleep(.3)

    #synclist.subscribe_list("global_test")

    time.sleep(.3)

    print("resulting items:", test_sl.items)





if __name__ == '__main__':
    defopt.run(main)