# Manos Dimogerontakis

import signal

import pox
from pox.core import core
from pox.lib.util import dpid_to_str

import slice
import db
import dbpoll
import threading

log = core.getLogger()




    
    #match = of.ofp_match()
    #match.dl_src = 
    #fm = of.ofp_flow_mod()
    #fm.match = match

#def sig_handler(signum, frame):
#    log.debug('SIGUSR1 caught')
    # fucking open is not working with signals
#    f = open('/dev/shm/Pongo','r')
    #f = io.open('/dev/shm/Pongo', 'r')
#    node1 = f.read()
    #node1 = node1[:-1]
#    log.debug('node1')
#    log.debug(node1)
    #node2 = f.readline()
#    f.close()
    #log.debug('node2')
    #log.debug(node2)

#signal.signal(signal.SIGUSR2, sig_handler)
#log.info('Handler connected')




class Test1(object) :


    def __init__(self):
        log.debug('My Test initiated')
        #all_nodes = Node.objects.all()
        #log.info(all_nodes)
        self.slice = None
        self.poll = None
        core.openflow.addListeners(self)
        core.addListener(pox.core.GoingUpEvent, self.start_event_loop)
        #t = threading.Thread(target=dbpoll.Dbpoll())
        #t.daemon = True
        #t.start()

    def start_event_loop(self,event):
        log.debug('Went Up')
        # Ideally i should wait until the http requests succeed on startup
        # orelse I get an empty switch in Connection_up
        self.slice = slice.MySlice()
        log.debug(self.slice)
        self.poll = dbpoll.Dbpoll()


    def _handle_ConnectionUp (self, event):
        log.debug("Switch %s has come up.", dpid_to_str(event.dpid))
        ports = event.ofp.ports
        log.debug(ports)
        # Debug hw_addr
        for p in ports:
            #TODO Naming schema for switches
            if p.name == 'br0' or p.name == 'br1' or p.name == 'br2':
                switch = p.hw_addr
                log.debug(type(switch))
        log.debug('The switch address is')
        log.debug(switch)
        node = self.slice.find_switch(str(switch))
        sliver = self.slice.sliver_on_node(node)
        log.debug("Switch is on sliver "+sliver+" in node "+node)
        db.create_sliver(sliver,node,event.dpid,str(switch))




def launch ():
  log.debug('1')
  core.registerNew(Test1)
