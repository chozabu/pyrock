"""websockets_ui.py: Provides an interface at various levels to allow construction
 of a user interface or app over websockets."""

__author__ = "Alex 'Chozabu' P-B"
__copyright__ = "Copyright 2016, Chozabu"

from threading import Thread
from time import sleep


import asyncio
import datetime
import random
import websockets


import machine
import settings
import synclist

from apps import basic_chat, forums

connected = set()
serve_port = 5678

async def time(websocket, path):
    connected.add(websocket)
    while True:
        data = await websocket.recv()
        print("got", data)
        now = datetime.datetime.utcnow().isoformat() + 'Z' + str(connected)
        await websocket.send(now + data)
        #await asyncio.sleep(random.random() * 3)


def _init():
    print("WSUI on port", serve_port)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    start_server = websockets.serve(time, '127.0.0.1', serve_port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

def init():
    print("WSUI will be on port", serve_port)
    t=Thread(
        target=_init,
        kwargs={})
    t.daemon=True
    t.start()
