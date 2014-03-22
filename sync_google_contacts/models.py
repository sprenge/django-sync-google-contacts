#!/usr/bin/env python

from django.db import models
from bitfield import BitField
import datetime
import time

class GoogleAdminAccounts(models.Model):
    #user = models.OneToOneField(User)
    priority = models.IntegerField(unique=True)
    password = models.CharField(max_length=80)
    email = models.CharField(max_length=128, blank=True)
    flags = BitField(flags=('tbc',),blank=True)
    enable = models.BooleanField(default=True)
    last_changed = models.DateTimeField(default=datetime.datetime.fromtimestamp(time.mktime(time.strptime("01/01/1970 01:00:00",  "%d/%m/%Y %H:%M:%S"))))

    def __unicode__(self):
        return u'%s' % (self.email)

