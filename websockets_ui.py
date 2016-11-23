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
import network
import json


import machine
import settings
import synclist

from apps import basic_chat, forums

connected = set()
serve_port = 5678

async def handle(websocket, path):
    connected.add(websocket)
    while True:
        try:
            data = await websocket.recv()
            jdata=None
            try:
                jdata = json.loads(data)
            except:
                await websocket.send("sorry, couldn't decode that json!")
            print("got", data)
            if jdata:
                intent = jdata.get("intent")
                if not intent:
                    await websocket.send("you must give an 'intent'")
                else:
                    if intent == "ping":
                        await websocket.send("pong")
                    elif intent == "broadcast":
                        basic_chat.send_message(jdata['message'])
                        await websocket.send(json.dumps({"OK":"OK"}))
                    elif intent == "get_chat":
                        await websocket.send(json.dumps(basic_chat.messagelist))
                    elif intent == "get_forums":
                        await websocket.send(json.dumps([(f.name, f.id) for f in forums.forums]))


            now = datetime.datetime.utcnow().isoformat() + 'Z' + str(connected)

        except websockets.exceptions.ConnectionClosed as e:
            if websocket in connected:
                connected.remove(websocket)
                print("WS client disconnected")
            else:
                print("Unknown WS client disconnected")
            break


def _init():
    print("WSUI on port", serve_port)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    start_server = websockets.serve(handle, '127.0.0.1', serve_port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def got_chat_msg(data, machine, meta):
    try:
        loop = asyncio.get_event_loop()
    except:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(pump_msg(data))
    except Exception as e:
        print(e)
        print("websoockets api failed to start")


async def pump_msg(data):
    remlist = []
    for c in connected:
        try:
            await c.send(str(data))
        except websockets.exceptions.ConnectionClosed as e:
            remlist.append(c)
            print("WS client disconnected")
    for r in remlist:
        connected.remove(r)


def init():
    network.hook_type("basic_chat", got_chat_msg)
    print("WSUI will be on port", serve_port)
    t=Thread(
        target=_init,
        kwargs={})
    t.daemon=True
    t.start()
