#synclist provides a high level list of dicts/json self.items
#it should be able to use multiple underlying transports

import machine, network

synclists = {}

def init():
    network.hook_type("synclist", on_recv_item)

def create_synclist(id):
    sl = SyncList(id)
    synclists[id] = sl
    return sl

def on_recv_item(data, sender):
    print("Got sync related item:", data, sender)
    meta = data['meta']
    data = data['data']
    slid = data['id']
    sl = synclists[slid]
    if meta['subtype'] == "subscribe":
        sl.subscribe(sender)
        sl.sync_to_contact(sender.pkey)
    if meta['subtype'] == "syncitem":
        print("SYNCITEM")
        sl.on_recv_item(sender.pkey, data)
    print(sl.items)

def subscribe_list(id):
    machine.send_all({"id":id},{"type":"synclist", "subtype":"subscribe"})


class SyncList:
    def __init__(self, ownid="testid"):
        self.ownid = ownid
        self.items_by_recv_date = []
        self.items = {}
        self.subscribers = {}
        #subscribers[self.ownid] = {'last_sync':0}


    def on_recv_item(self, cId, item):
        #contact = self.subscribers[cId]
        if item['hash'] not in self.items:
            self.items_by_recv_date.append(item)
            self.items[item['hash']] = item
    
    def publish_item(self, item):
        item['hash'] = hash(str(item))
        self.on_recv_item(self.ownid, item)

    def subscribe(self, m):
        self.subscribers[m.pkey] = {'last_sync':0, "machine": m}
        self.sync_to_contact(m.pkey)

    def _send_item(self, contact, item):
        item['id'] = self.ownid
        m = machine.machines_dict[contact]
        print(contact)
        print(item)
        print("sending" + str(item) + " to " + str(contact), m)
        m.send_packet(item, {"type": "synclist", "subtype": "syncitem"})


    #get contact up to date with own data
    def sync_to_contact(self, cId):
        contact = self.subscribers[cId]
        ls = contact['last_sync']
        for i in self.items_by_recv_date[ls:]:
            self._send_item(cId, i)
            print("sent")
        #should confirm contact has got data, then:
        contact['last_sync'] = len(self.items_by_recv_date)

    def sync_to_all(self):
        for c in self.subscribers.keys():
            self.sync_to_contact(c)
