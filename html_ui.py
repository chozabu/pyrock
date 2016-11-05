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

from apps import basic_chat, forums

header = '''
<h1>PyRock</h1>
<a href="/">home</a>
<a href="/chat/">chat</a>
<a href="/forums/">forums</a>
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
        #print(retstr)
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
        #print(retstr)
        return retstr.encode()
class Forums(resource.Resource):
    isLeaf = True

    def render_GET(self, request):

        print(request.args)

        if b'newforum' in request.args:
            forumid = request.args[b'newforum'][0].decode()
            print(forumid)
            forums.create_forum(forumid)
            request.redirect("/forums")
            #request.finish()
            return b"no"

        if b'newpost' in request.args:
            forumid = request.args[b'forumid'][0].decode()
            newpost = request.args[b'newpost'][0].decode()
            forum = forums.forums_dict[forumid]
            forum.create_post({"message": newpost})
            request.redirect("/forums/?view="+forumid)
            #request.finish()
            return b"no"

        retstr = "<html>"
        retstr += header
        retstr += "<h2>Forums</h2>"
        retstr += "<h4>This machine is: " + settings.machine_name + "</h4>"

        request.setHeader("Content-Type", "text/HTML; charset=utf-8")
        if not request.args:#b'view' not in request.args:
            retstr += "<ul>"
            for m in forums.forums:
                retstr += '<li> <a href="?view=' + str(m.name) + '">' + str(m.name) + '</a></li>'
            retstr += "</ul>"

            retstr += '''
                <form action="forums">
                  <input type="text" name="newforum" value="" placeholder="type forum name here" autofocus="autofocus"><br>
                  <input type="submit" value="Submit">
                </form>
            '''
            retstr += "</html>"
            return retstr.encode()

        if b'view' in request.args:#not request.args:
            forumid = request.args[b'view'][0].decode()
            forum = forums.forums_dict[forumid]
            retstr += "<h1>" + forum.name + "</h1>"
            retstr += "<ul>"
            for m in forum.get_posts():
                retstr += '<li>' + str(m) + '</li>'
            retstr += "</ul>"

            retstr += "<ul>"
            for m in forum.items.subscribers:
                retstr += '<li>' + str(m) + '</li>'
            retstr += "</ul>"

            retstr += '''
                <form action="forums">
                  <input type="hidden" name="forumid" value="''' + forumid + '''" >
                  <input type="text" name="newpost" value="" placeholder="type message here" autofocus="autofocus"><br>
                  <input type="submit" value="Submit">
                </form>
            '''
            retstr += "</html>"
            return retstr.encode()


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
        #print(retstr)
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
        #print(retstr)
        return retstr.encode()
#site = server.Site(Simple())
#reactor.listenTCP(8080, site)
#reactor.run()


def init(serve_port=None):
    if not serve_port:
        serve_port = settings.ui_port
    root = resource.Resource()
    root.putChild(b"", Simple())
    root.putChild(b"chat", Chat())
    root.putChild(b"forums", Forums())
    root.putChild(b"quit", Quit())
    #root.putChild(b"book", Book())
    site = server.Site(root)
    endpoints.serverFromString(reactor, "tcp:"+str(serve_port)).listen(site)
    #print("starting networking thread")
    t=Thread(
        target=reactor.run,
        kwargs={'installSignalHandlers':False})
    t.daemon=True
    print("UI on port", serve_port)
    #t.start()
    #print("running")

if __name__ == "__main__":
    init()
    while 1:
        sleep(60)
        print("Still running")
