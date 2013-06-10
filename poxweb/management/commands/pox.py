from django.core.management.base import NoArgsCommand, make_option

#import runpy
#from pox import Pox

class Command(NoArgsCommand):
    help = "Whatever you want to print here"

    def handle_noargs(self, **options):
        #import sys
        #sys.path.append('poxweb/pox/')
        #from pox.boot import boot
        #boot()
        p = Pox()


        
