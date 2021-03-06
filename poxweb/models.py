from django.db import models

from django.core.exceptions import ValidationError


class Flow(models.Model):
    internalip = models.CharField(max_length=200)
    externalip = models.CharField(max_length=200)
    internalport = models.IntegerField()
    externalport = models.IntegerField()
    idletime = models.IntegerField()
    hardtime = models.IntegerField()
    
    def __unicode__(self):
        return "Internal: IP=" + self.internalip + " port=" +\
                str(self.internalport) +", External: IP=" + self.externalip\
                +  " port=" + str(self.externalport)

class User(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


# Each dpid/Switch represents one node
class Sliver(models.Model):
    
    #def save(self, *args, **kwargs):
    #    super(Node, self).save(*args, **kwargs)

    
    sliver_id = models.CharField(max_length=200, unique=True)
    node_id = models.CharField(max_length=200)
    dpid = models.CharField(max_length=200)
    switch_mac = models.CharField(max_length=200)

    def __unicode__(self):
        return self.sliver_id

class Link(models.Model):

    #LINK_STATE = (
    #    ('up','Up'),
    #    ('down','Down'),
    #)
    sliver1 = models.ForeignKey(Sliver, null=True, unique=False, related_name='sliver1')
    sliver2 = models.ForeignKey(Sliver, null=True, unique=False, related_name='sliver2')
    #state = models.CharField(max_length=4, choices=LINK_STATE)

    def __unicode__(self):
        return "sliver"+self.sliver1.sliver_id + "_to_sliver" + self.sliver2.sliver_id


    def clean(self):
        if self.sliver1 == self.sliver2:
             raise ValidationError("You cannot create a link between a node" +\
                     " and itself")
             super(Link, self).clean()


