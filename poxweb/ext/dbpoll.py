import db
import time

import pox
from pox.core import core
from pox.lib.recoco.recoco import *
from pox.lib.util import dpid_to_str
import pox.openflow.libopenflow_01  as of
from pox.lib.addresses import EthAddr

log = core.getLogger()


class Dbpoll(Task) :

    def __init__ (self):
        Task.__init__(self)    
        # I don't know why the following thins are not printed :-(
        log.debug("Links:::::")
        #self.links = db.get_links()
        log.debug("Links:::::")
        #self.links = self.objList2dict(links)
        #log.debug(self.links)
        Task.start(self)

    def run(self):
        oldlinks = db.get_links()
        while True:
            log.debug('loop')
            newlinks = db.get_links()
            if len(newlinks) < len(oldlinks):
                log.debug("New Links")
                #newlinks = self.objList2dict(newlinks)
                log.debug(newlinks)
                # Find the deleted links
                dellinks = []
                for link in oldlinks:
                    if link not in newlinks:
                        log.debug('Del link')
                        log.debug(link)
                        dellinks.append(link)
                log.debug('Deleted Links')
                log.debug(dellinks)
                # Get info from the deleted links
                for link in dellinks:
                    # This is the db representation id for sliver 1
                    sliver1 = str(link['sliver1_id'])
                    # We use it to get sliver1 info from db
                    sliver1 = db.get_sliver(sliver1)
                    # Now sliver one has the db data
                    log.debug(sliver1)
                    node1= str(sliver1['node_id'])
                    log.debug(node1)
                    log.debug(dpid_to_str(int(sliver1['dpid'])))
                    node1dpid = int((sliver1['dpid']))
                    node1mac = str(sliver1['switch_mac'])
                    log.debug('First nodes dpid')
                    log.debug(node1dpid)
                    sliver2 = str(link['sliver2_id'])
                    sliver2 = db.get_sliver(sliver2)
                    node2= str(sliver2['node_id'])
                    node1dpid = int((sliver2['dpid']))
                    node2mac = str(sliver1['switch_mac'])
                    log.debug(node2)
                    for connection in core.openflow.connections:
                        if connection.dpid == node1dpid :
                            log.debug('Got you!')
                            # Block in Node 1 incoming from node 2
                            fm = of.ofp_flow_mod()
                            fm.match.dl_src = EthAddr(node2mac)
                            #fm.actions.append(of.ofp_action_output( port=of.OFPP_NONE ))
                            connection.send(fm)
                            # Block in Node 1 outcoming to node 2
                            fm = of.ofp_flow_mod()
                            fm.match.dl_dst = EthAddr(node2mac)
                            #fm.actions.append(of.ofp_action_output( port=of.OFPP_NONE ))
                            connection.send(fm)

            # Outside the if to catch also new links
            # not only dropped ones
            oldlinks = newlinks
            time.sleep(5)



    def objList2dict(self,objList):
        dictList = []
        for obj in objList:
            dictList.append(obj.__dict__)
        return dictList
    

def launch ():
    core.registerNew(Dbpoll)
