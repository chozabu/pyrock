"""Foobar.py: Description of what foobar does."""

__author__ = "Alex 'Chozabu' P-B"
__copyright__ = "Copyright 2016, Chozabu"


import network, machine
import settings

messagelist = []


def init(root):
    network.hook_type("basic_chat", got_data)

def got_data(data, machine):
    print(settings.machine_name, data, machine.name)
    messagelist.append(machine.name + ": " + data['message'])


def send_message(message):
    messagelist.append(settings.machine_name + ": " + message)
    machine.send_all({"message": message}, {"type":"basic_chat"})

