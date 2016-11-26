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

import debugprint

import random

inittime = time.time()

def test_cb(data, sender, meta):
    print(settings.machine_name, "MAINCB", data, sender, sender.ip, sender.name)

def main(settingsfile="settings.json", test_mode=False, no_auto=False):
    """Display a friendly greeting.

    :param str settingsfile: settings file to load
    :param bool test_mode: True to run some tests
    :param bool no_auto: True disable auto FR
    """

    #load settings
    with open(settingsfile) as data_file:
        data = json.load(data_file)
        settings.load_data(data)
        machinesfile = data['machines_file']

    #init network
    network.init(settings.serve_port)
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

    #load machines
    machine.init()
    if not no_auto:
        machine.autoconnect()

    #connect to all?

    print("Init Complete")

    if test_mode:
        run_tests()

    while settings.running:
        time.sleep(1)


def run_tests():
    print(settings.machine_name, "ready to run tests")
    while time.time() < inittime+1:
        time.sleep(0.01)
    print(settings.machine_name, "Running tests")
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
    print(inittime)





if __name__ == '__main__':
    defopt.run(main)