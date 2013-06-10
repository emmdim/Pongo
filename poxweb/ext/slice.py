import requests
import json

from types import IntType,StringType

myslice = 51
prefix = "https://controller.community-lab.net/api/"
slice_url = prefix + "slices/"+str(myslice)

def node_url(node_id):
    if isinstance(node_id,StringType) :
        #print "String"
        return prefix + "nodes/" + node_id
    if isinstance(node_id,IntType) :
        #print "Int"
        return prefix + "nodes/" + str(node_id)



# Get a python dict with the properties of the node
def get_node_data(node_id):
    payload = {'format':'json'}
    url = node_url(node_id)
    #print url
    r = requests.get(url, params=payload)
    #print r.content
    data = json.loads(r.content)
    #print type(data)
    return data


def get_slice_data():
    payload = {'format':'json'}
    url = slice_url
    print url
    r = requests.get(url, params=payload)
    #print r.content
    data = json.loads(r.content)
    #print type(data)
    return data


def get_sliver_data(url):
    payload = {'format':'json'}
    r = requests.get(url, params=payload)
    #print r.content
    data = json.loads(r.content)
    #print type(data)
    return data


def get_slivers_from_slices():
    slice_data = get_slice_data()
    slivers_urls=[]
    for sliver in slice_data['slivers']:
        temp = str(sliver['uri'])
        slivers_urls.append(temp)
    return slivers_urls

def get_node_from_sliver(sliver_url):
    sliver_data = get_sliver_data(sliver_url)
    node_url = sliver_data['node']['uri']
    return node_url

def get_switch_node(switch,nodes):
    for n in nodes:
        node_data = get_node_data(n)
        switch1 = str(node_data['properties']['switch_mac'])
        if switch1 == switch:
            return str(n)



class MySlice :

    def __init__(self):

        # Get Nodes and Slivers
        slivers_urls = get_slivers_from_slices()
        slivers = []
        for s in slivers_urls:
            base = prefix + "slivers/"
            slivers.append(s[len(base):])
        nodes_urls = []
        for s in slivers_urls:
            nodes_urls.append(str(get_node_from_sliver(s)))
        print nodes_urls
        nodes = []
        for n in nodes_urls :
            print n
            base = prefix + "nodes/"
            nodes.append(n[len(base):])
        # nodes and slivers urls are related one by one
        self.slivers = slivers
        self.nodes  = nodes

        print slivers
        print nodes
        

    def find_switch(self,switch):
        nodes = self.nodes
        n = get_switch_node(switch,nodes)
        print "Switch " + switch + "is in node " + n
        return n

    def test_switches(self):
        # Test the switch 
        switches = ['46:5f:c3:a0:e9:4e','9a:8d:ad:de:77:43','4a:43:c2:76:d6:48']
        for s in switches:
            self.find_switch(s)


    def sliver_on_node(self,node):
        index = self.nodes.index(node)
        return self.slivers[index]

