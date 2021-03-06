from poxweb.models import Sliver, Link

### SLIVER

def get_slivers():
    return Sliver.objects.values()

# Get the dict form of a sliver object
def get_sliver(sliver_id):
    return Sliver.objects.get(id=sliver_id).__dict__


# Create a Sliver model
def create_sliver(sliver_id,node_id,dpid,switch_mac):
    s = Sliver(sliver_id=sliver_id , node_id=node_id, dpid=dpid, switch_mac=switch_mac)
    s.save()
    for s1 in Sliver.objects.all():
        if s != s1:
            #log.debug(s.__unicode__())
            #log.debug(s1.__unicode__())
            add_link(s,s1)


def delete_sliver(dpid):
    sid = Sliver.objects.get(dpid=dpid)
    print sid
    sid = sid.id
    print sid
    for link in Link.objects.all():
        if link.sliver1 == sid or link.sliver2 == sid:
            print link.__unicode__()
            link.delete()
    Sliver.objects.get(id=sid).delete()
    #s = Sliver(sliver_id=sliver_id , node_id=node_id, dpid=dpid, switch_mac=switch_mac)
    #s.save()
    #for s1 in Sliver.objects.all():
    #    if s != s1:
    #        #log.debug(s.__unicode__())
    #        #log.debug(s1.__unicode__())
    #        add_link(s,s1)

# Get all the info from a sliver model
# The sliver_id argument is the id of the model
# in the db
def get_sliver_info(sliver_id):
    sliver = get_sliver(sliver_id)
    sliverID = sliver['sliver_id']
    nodeID = sliver['node_id']
    dpid = sliver['dpid']
    switch_mac = sliver['switch_mac']
    return str(sliverID), str(nodeID), int(dpid), str(switch_mac)

### LINK

# Get all links in dict form
def get_links():
    return Link.objects.values()



# Add new link
def add_link(sliver1, sliver2):
    s = Link(sliver1=sliver1 , sliver2=sliver2)
    s.save()
