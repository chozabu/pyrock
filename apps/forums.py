#forum app puesdo code:

from synclist import SyncList
import network
import settings

forums = []
forums_dict = {}


def init(root):
    network.hook_type("forum", got_data)

def got_data(data, machine):
    print(settings.machine_name, data, machine.name)

def createForum(forumname):
    new_forum = Forum(forumname, forumname)
    forums.push(new_forum)
    forums_dict[forumname] = new_forum

class Forum():
    def __init__(self, name="testforum", id="testid"):
        self.items = SyncList()
        self.name = name
        self.id = id
    def create_post(self, item):
        self.items.push(item)
        self.items.sync_all()
    def get_posts(self):
        return self.items.items

def testing():
    p1 = createPost(myforum, title="testingtitle", body="something")
    createPost(myforum, title="testingtitle", body="something", parent=p1)


    