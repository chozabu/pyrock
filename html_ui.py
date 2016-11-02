"""Foobar.py: Description of what foobar does."""

__author__ = "Alex 'Chozabu' P-B"
__copyright__ = "Copyright 2016, Chozabu"

from threading import Semaphore, Thread
from time import sleep
from twisted.web import server, resource
from twisted.internet import protocol, reactor, endpoints

import machine, synclist, forums, settings

class Simple(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        request.setHeader("Content-Type", "text/HTML; charset=utf-8")

        retstr = "<html>"
        retstr += "<h1>PyRock UI</h1>"
        retstr += "<h4>This machine is: " + settings.machine_name + "</h4>"

        retstr += "<h3>Friends</h3>"
        retstr += "<ul>"
        for m in machine.machines:
            retstr += "<li>" + m.name + " (" + m.ip + ")</li>"
        retstr += "</ul>"

        retstr += "<h3>Synclists</h3>"
        retstr += "<ul>"
        for l in synclist.synclists.values():
            print("!!!", l)
            retstr += "<li>" + l.ownid + " (" + str(l.items) + ")</li>"
        retstr += "</ul>"

        retstr += "</html>"
        print(retstr)
        return retstr.encode()

#site = server.Site(Simple())
#reactor.listenTCP(8080, site)
#reactor.run()


def init(serve_port=8080):
    site = server.Site(Simple())
    endpoints.serverFromString(reactor, "tcp:"+str(serve_port)).listen(site)
    #print("starting networking thread")
    t=Thread(
        target=reactor.run,
        kwargs={'installSignalHandlers':False})
    t.daemon=True
    t.start()
    #print("running")

if __name__ == "__main__":
    init()
    while 1:
        sleep(60)
        print("Still running")
