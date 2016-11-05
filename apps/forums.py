#forum app puesdo code:

import synclist
import network
import settings

forums = []
forums_dict = {}


def init(root):
    network.hook_type("forum", got_data)

def got_data(data, machine, meta):
    print(settings.machine_name, data, machine.name)

def create_forum(forumname):
    print("creating forum", forumname)
    if forumname in forums_dict:
        new_forum = forums_dict[forumname]
        synclist.subscribe_list(new_forum.id)
    else:
        new_forum = Forum(forumname, forumname)
        forums.append(new_forum)

    forums_dict[forumname] = new_forum

class Forum():
    def __init__(self, name="testforum", id="testid"):
        self.items = synclist.SyncList(ownid=id)
        self.name = name
        self.id = id
    def create_post(self, item):
        self.items.publish_item(item)
        self.items.sync_to_all()
    def get_posts(self):
        return self.items.items_by_recv_date

def testing():
    p1 = createPost(myforum, title="testingtitle", body="something")
    createPost(myforum, title="testingtitle", body="something", parent=p1)
