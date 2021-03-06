"""Foobar.py: Description of what foobar does."""

__author__ = "Alex 'Chozabu' P-B"
__copyright__ = "Copyright 2016, Chozabu"


from twisted.internet import protocol, reactor, endpoints

from threading import Semaphore, Thread
from time import sleep
import socket, json
import sys

import machine

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import requests
import cgi


# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        print("Get HTTP request made")
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = "Hey, you should POST some json with the correct formatting to this endpoint!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        rfile = self.rfile.read(length)
        print()
        jdata = json.loads(rfile.decode('utf-8'))
        print("POSTED", jdata)
        sender = machine.machines_dict.get(jdata['meta']['pkey'])
        on_recv_data(jdata, sender)
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = "Hello POST world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


def run(port=None):
    print('starting server...')
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


def send_data(HOST, PORT, data):
    PORT = PORT + 10
    print("sendingHTTP", HOST, PORT, data)

    #received = requests.post("http://localhost" + ":" + str(PORT), data=data)
    try:
        received = requests.post("http://" + HOST+":"+str(PORT), data=data)
    except Exception as e:
        print(e)
        print("HTTP failed to send data", HOST, PORT, data)
        return 0, "fail"
    return 1, received

def on_recv_data(data, sender):
    pass

def send_packet(HOST, PORT, data, meta):
    packet = json.dumps({"data":data, "meta":meta})
    ret = send_data(HOST,PORT, packet)
    return ret


def init(serve_port):
    t=Thread(target=run,
             kwargs={'port': serve_port})
    t.daemon=True
    t.start()
    print("HTTP network listening on", serve_port)

if __name__ == "__main__":
    init()
    while 1:
        sleep(60)
        print("Still running")
