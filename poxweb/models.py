from django.db import models

# Create your models here.

class Flow(models.Model):
 internalip = models.CharField(max_length=200)
 externalip = models.CharField(max_length=200)
 internalport = models.IntegerField()
 externalport = models.IntegerField()
 idletime = models.IntegerField()
 hardtime = models.IntegerField()
 def __unicode__(self):
  return "Internal: IP=" + self.internalip + " port=" + str(self.internalport) +", External: IP=" + self.externalip +  " port=" + str(self.externalport)

class User(models.Model):
 name = models.CharField(max_length=200)

class Device(models.Model):
 dpid = models.CharField(max_length=200)
