# Copyright 2011 James McCauley
#
# This file is part of POX.
#
# POX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# POX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with POX.  If not, see <http://www.gnu.org/licenses/>.


# This file also contains additions described here:
# http://pieknywidok.blogspot.com.es/2012/08/djangoflow-part-two-quick-and-simple-ui.html
# that concern the integration of POX with django


# Further additions are made by Manos Dimogerontakis


"""
An L2 learning switch.

It is derived from one written live for an SDN crash course.
It is somwhat similar to NOX's pyswitch in that it installs
exact-match rules for each flow.
"""

#from django.core.management import setup_environ
#import sys
#sys.path.append('./')
#import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'GenServer.settings'
#from django.conf import settings
#from Pongo import settings
#setup_environ(settings)

#from django.core import signals
from django.db.models.signals import pre_save
from django.dispatch import receiver
from poxweb.models import Node, Link

import signal

from pox.core import core

log = core.getLogger()

# We don't want to flood immediately when a switch connects.
# Can be overriden on commandline.


#@receiver(pre_save, sender=Node, dispatch_uid='app.poxweb.test')
#def my_handler(sender, **kwargs):
#        log.debug('New Node')
def my_handler(sender, **kwargs):
    print 'New Node'
    log.info('New Node')


def sig_handler(signum, frame):
    log.debug('SIGUSR1 caught')

signal.signal(signal.SIGUSR1, sig_handler)

print "Hi"
pre_save.connect(my_handler,sender=Node)

class Test1(object) :

    def __init__(self):
        log.debug('My Test initiated')
        all_nodes = Node.objects.all()
        log.info(all_nodes)
        pre_save.connect(my_handler,weak=False)
        log.info('Handler connected')

def launch ():
  log.debug('1')
  core.registerNew(Test1)
