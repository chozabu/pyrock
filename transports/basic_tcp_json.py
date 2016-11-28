"""Foobar.py: Description of what foobar does."""

__author__ = "Alex 'Chozabu' P-B"
__copyright__ = "Copyright 2016, Chozabu"


from twisted.internet import protocol, reactor, endpoints

from threading import Semaphore, Thread
from time import sleep
import socket, json
import sys

import machine

csocklist = {}

def send_data(HOST, PORT, data):
    global csocklist
    print("sendingTCP", HOST, PORT, data)

    try:
        # Create a socket (SOCK_STREAM means a TCP socket)
        id_string = str(HOST) + ':' + str(PORT)
        sock = csocklist.get(id_string, None)
        if not sock:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            sock.settimeout(1)
            # Connect to server and send data
            sock.connect((HOST, PORT))
            csocklist[id_string] = sock
        sock.sendall(bytes(data + "\n", "utf-8"))

        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")

        #print("Sent:     {}".format(data))
        #print("Received: {}".format(received))
    except Exception as e:
        print("TWISTED failed to send data", HOST, PORT, data)
        print(e)
        return 0, "fail"
    return 1, received

def on_recv_data(data, sender):
    pass

def send_packet(HOST, PORT, data, meta):
    packet = json.dumps({"data":data, "meta":meta})
    ret = send_data(HOST,PORT, packet)
    return ret

class Echo(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.append(self)

    #def dataReceived(self, data):
    #    for echoer in self.factory.clients:
    #        echoer.transport.write(data)

    def connectionLost(self, reason):
        print("Connection lost!", self)
        self.factory.clients.remove(self)
    def dataReceived(self, data):
        #print("echoing: ", data)
        #print(json.loads(data.decode()))
        try:
            jdata = json.loads(data.decode())
        except:
            self.transport.write(
                json.dumps(
                    {
                        "data":{"message": data.decode()},
                        "meta":{"error":"could not understand message"}
                    }
                ).encode()
            )
            return
        #ip, port = self.transport.client
        #print(ip, port)
        #print(str(self.transport.getPeer()))
        #sender = machine.get_by_ip(ip)
        sender = machine.machines_dict.get(jdata['meta']['pkey'])
        on_recv_data(jdata, sender)

        self.transport.write("OK".encode('utf-8'))

class EchoFactory(protocol.Factory):
    clients = []
    def buildProtocol(self, addr):
        client = Echo(self)
        EchoFactory.clients.append(client)
        return client

def init(serve_port):
    endpoints.serverFromString(reactor, "tcp:"+str(serve_port)).listen(EchoFactory())
    #print("starting networking thread")
    t=Thread(
        target=reactor.run,
        kwargs={'installSignalHandlers':False})
    t.daemon=True
    t.start()
    print("basic network listening on", serve_port)

if __name__ == "__main__":
    init()
    while 1:
        sleep(60)
        print("Still running")
