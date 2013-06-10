import db
import time

import pox
from pox.core import core
from pox.lib.recoco.recoco import *
from pox.lib.util import dpid_to_str
import pox.openflow.libopenflow_01  as of
from pox.lib.addresses import EthAddr

log = core.getLogger()

# Every period seconds the db is queried
period = 5


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

    # The main loop of the task
    # Checks for deleted links
    def run(self):
        oldlinks = db.get_links()
        oldslivers = db.get_slivers()
        while True:
            log.debug('loop')
            newlinks = db.get_links()
            log.debug(len(oldlinks))
            log.debug(len(newlinks))
            newslivers = db.get_slivers()
            log.debug(len(oldslivers))
            log.debug(len(newslivers))
            if len(newlinks) < len(oldlinks) and len(oldslivers) == len(newslivers):
                log.debug("Rem Links")
                #newlinks = self.objList2dict(newlinks)
                log.debug(newlinks)
                # Find the deleted links
                dellinks = self.diff_list(oldlinks,newlinks)
                #log.debug('Deleted Links')
                #log.debug(dellinks)
                # Delete the removed links
                self.del_links(dellinks)
            elif len(newlinks) > len(oldlinks) and len(oldslivers) == len(newslivers):
                log.debug("Add Links")
                addlinks = self.diff_list(newlinks,oldlinks)
                log.debug(addlinks)
                self.add_links(addlinks)
            # Outside the if to catch also new links
            # not only dropped ones
            oldlinks = newlinks
            oldslivers = newslivers
            time.sleep(period)
    


    # returns the different elements of two lists
    def diff_list(self,l1,l2):
        diff = []
        for e in l1:
            if e not in l2:
                diff.append(e)
        return diff

    # Elliminate all the links in the list
    def del_links(self,links):
        # Get info from the deleted links
        for link in links:
            # This is the db representation id for sliver 1
            sliver1 = str(link['sliver1_id'])
            # Get all the info from the model
            sliver1,node1,dpid1,mac1 = db.get_sliver_info(sliver1)
            # This is the db representation id for sliver 1
            sliver2 = str(link['sliver2_id'])
            # Get all the info from the model
            sliver2,node2,dpid2,mac2 = db.get_sliver_info(sliver2)
            # Send the delete link OF messages
            self.of_send_link_down(dpid1,mac2)
            self.of_send_link_down(dpid2,mac1)

    def add_links(self,links):
        # Get info from the deleted links
        for link in links:
            log.debug('Inside add Links')
            # This is the db representation id for sliver 1
            sliver1 = str(link['sliver1_id'])
            # Get all the info from the model
            sliver1,node1,dpid1,mac1 = db.get_sliver_info(sliver1)
            # This is the db representation id for sliver 1
            sliver2 = str(link['sliver2_id'])
            # Get all the info from the model
            sliver2,node2,dpid2,mac2 = db.get_sliver_info(sliver2)
            # Send the delete link OF messages
            self.of_send_link_up(dpid1,mac2)
            self.of_send_link_up(dpid2,mac1)
    
    # Get mac from sliver model as dict
    def get_mac_from_sliver(self,sliver):
        return str(sliver['switch_mac'])



    # Send OF message to switch with DPID=dpid to block
    # connections with MAC=rmac
    def of_send_link_down(self,dpid,rmac):
        for connection in core.openflow.connections:
            if connection.dpid == dpid :
                # Parse rmac the OF way
                rmac = EthAddr(rmac)
                log.debug('Got you!')
                # Block in Node 1 incoming from node 2
                fm = of.ofp_flow_mod()
                fm.match.dl_src = rmac
                # Many OpenVswitch  versions do not support OFPP_NONE
                # Instead of the no action is defined
                # hence an empty action
                #fm.actions.append(of.ofp_action_output( port=of.OFPP_NONE ))
                connection.send(fm)
                # Block in Node 1 outcoming to node 2
                fm = of.ofp_flow_mod()
                fm.match.dl_dst = rmac
                #fm.actions.append(of.ofp_action_output( port=of.OFPP_NONE ))
                connection.send(fm)

    def of_send_link_up(self,dpid,rmac):
        for connection in core.openflow.connections:
            if connection.dpid == dpid :
                # Parse rmac the OF way
                rmac = EthAddr(rmac)
                log.debug('Got you!')
                # Block in Node 1 incoming from node 2
                fm = of.ofp_flow_mod()
                fm.match.dl_src = rmac
                fm.command = of.OFPFC_DELETE
                # Many OpenVswitch  versions do not support OFPP_NONE
                # Instead of the no action is defined
                # hence an empty action
                #fm.actions.append(of.ofp_action_output( port=of.OFPP_NONE ))
                connection.send(fm)
                # Block in Node 1 outcoming to node 2
                fm = of.ofp_flow_mod()
                fm.match.dl_dst = rmac
                fm.command = of.OFPFC_DELETE
                #fm.actions.append(of.ofp_action_output( port=of.OFPP_NONE ))
                connection.send(fm)
    
    
    # Convert Django dbobject to Dict List 
    def objList2dict(self,objList):
        dictList = []
        for obj in objList:
            dictList.append(obj.__dict__)
        return dictList
    
# In case we want it to be a pox component
#def launch ():
#    core.registerNew(Dbpoll)
