"""Foobar.py: Description of what foobar does."""

__author__ = "Alex 'Chozabu' P-B"
__copyright__ = "Copyright 2016, Chozabu"

from threading import Thread
from time import sleep

from twisted.internet import reactor, endpoints
from twisted.web import server, resource

import machine
import settings
import synclist

from apps import basic_chat

header = '''
<h1>PyRock</h1>
<a href="/">home</a>
<a href="/chat/">chat</a>
<a href="/quit/">quit</a>
'''


class Simple(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        request.setHeader("Content-Type", "text/HTML; charset=utf-8")

        retstr = "<html>"
        retstr += header
        retstr += "<h2>Home</h2>"
        retstr += "<h4>This machine is: " + settings.machine_name + "</h4>"
        retstr += '<a href="/quit/">Quit</a>'

        retstr += "<h3>Friends</h3>"
        retstr += "<ul>"
        for m in machine.machines:
            retstr += "<li>" + m.name + " (" + m.ip + ")</li>"
        retstr += "</ul>"

        retstr += "<h3>Synclists</h3>"
        retstr += "<ul>"
        for l in synclist.synclists.values():
            retstr += "<li>" + l.ownid + " (" + str(l.items) + ")</li>"
        retstr += "</ul>"

        retstr += "</html>"
        print(retstr)
        return retstr.encode()

class Chat(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader("Content-Type", "text/HTML; charset=utf-8")

        if b'newmessage' in request.args:
            print(str(request.args[b'newmessage'][0]))
            basic_chat.send_message(request.args[b'newmessage'][0].decode())
            request.redirect("/chat")
            #request.finish()
            return b"no"

        retstr = "<html>"
        retstr += header
        retstr += "<h2>Chat</h2>"
        retstr += "<h4>This machine is: " + settings.machine_name + "</h4>"

        retstr += '''
            <form action="chat">
              First name:<br>
              <input type="text" name="newmessage" value="" placeholder="type message here" autofocus="autofocus"><br>
              <input type="submit" value="Submit">
            </form>
        '''

        retstr += "<h3>messages</h3>"
        retstr += "<ul>"
        for m in basic_chat.messagelist:
            retstr += "<li>" + str(m) + "</li>"
        retstr += "</ul>"

        retstr += "</html>"
        print(retstr)
        return retstr.encode()
class Quit(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader("Content-Type", "text/HTML; charset=utf-8")
        settings.running = False

        retstr = "<html>"
        retstr += "<h1>PyRock Quitting</h1>"
        retstr += 'Goodbye'
        retstr += "</html>"
        print(retstr)
        return retstr.encode()
#site = server.Site(Simple())
#reactor.listenTCP(8080, site)
#reactor.run()


def init(serve_port=8080):
    root = resource.Resource()
    root.putChild(b"", Simple())
    root.putChild(b"chat", Chat())
    root.putChild(b"quit", Quit())
    #root.putChild(b"book", Book())
    site = server.Site(root)
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
