#!/usr/bin/env python

from django.db import models
from bitfield import BitField

class GoogleAdminAccounts(models.Model):
    #user = models.OneToOneField(User)
    priority = models.IntegerField(unique=True)
    password = models.CharField(max_length=80)
    email = models.CharField(max_length=128, blank=True)
    flags = BitField(flags=('tbc',),blank=True)

    def __unicode__(self):
        return u'%s' % (self.email)

