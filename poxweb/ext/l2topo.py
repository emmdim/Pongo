# Manos Dimogerontakis

import pox
from pox.core import core
from pox.lib.util import dpid_to_str

import slice
import db
import dbpoll

log = core.getLogger()
    

class L2topo(object) :
    """
    This POX application is strongly connected with two other 
    components: Django, and the CONFINE project. 
    
    We assume that when switches connec to POX they are fully
    connected with each other. Then, user will be able to 
    choose from the Django interface which link to drop.
    
    The goal of this app is to let the users choose from a
    django admin interface the topology of their switches.
    Small part of the functionality is implemented for
    now but it is a start.
    
    As you can see, slice ID is a parameter that is used to 
    get information about the nodes that contain the switches.
    These part is customized to suit the CONFINE prohect.

    """

    def __init__(self):
        log.debug('My Test initiated')
        self.slice = None
        self.poll = None
        core.openflow.addListeners(self)
        # Finish the rest of the initializations after the GoingUpEvent
        # is raised for safety
        core.addListener(pox.core.GoingUpEvent, self.finish_init)

    # Finish initializations
    def finish_init(self,event):
        log.debug('Went Up')
        # Ideally i should wait until the http requests succeed on startup
        # orelse I get an empty switch in Connection_up
        self.slice = slice.MySlice()
        log.debug(self.slice)
        self.poll = dbpoll.Dbpoll()

    # Called everytime a switch is connected
    def _handle_ConnectionUp (self, event):
        log.debug("Switch %s has come up.", dpid_to_str(event.dpid))
        ports = event.ofp.ports
        dpid = event.dpid
        log.debug(ports)
        
        # Find OF switch address
        for p in ports:
            #TODO Naming schema for switches
            if p.name == 'br0' or p.name == 'br1' or p.name == 'br2':
                switch = p.hw_addr
                #log.debug(type(switch))
        log.debug('The switch address is')
        log.debug(switch)
        # Register in DB the related to the switch CONFINE info
        self.confine_register(switch,dpid)

    # Find info abou the CONFINE node and sliver where the switch
    # is located, and store them in Django db
    def confine_register(self,switch,dpid):
        node = self.slice.find_switch(str(switch))
        sliver = self.slice.sliver_on_node(node)
        log.debug("Switch is on sliver "+sliver+" in node "+node)
        db.create_sliver(sliver,node,dpid,str(switch))

    def _handle_ConnectionDown (self, event):
        log.debug("Switch %s has gone up.", dpid_to_str(event.dpid))
        #ports = event.ofp.ports
        dpid = event.dpid
        #log.debug(ports)
        
        # Find OF switch address
        #for p in ports:
            #TODO Naming schema for switches
        #    if p.name == 'br0' or p.name == 'br1' or p.name == 'br2':
        #        switch = p.hw_addr
                #log.debug(type(switch))
        #log.debug('The switch address is')
        #log.debug(switch)
        # Register in DB the related to the switch CONFINE info
        self.confine_deregister(dpid)
    
    def confine_deregister(self,dpid):
        db.delete_sliver(str(dpid))

def launch (slice_id = 51):
  log.debug('1')
  core.registerNew(L2topo)
