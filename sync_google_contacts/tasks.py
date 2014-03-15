#!/usr/bin/env python

from datetime import timedelta
from celery.task import PeriodicTask

class pull_contacts_from_google(PeriodicTask):
    run_every = timedelta(seconds=15)

    def run(self, **kwargs):
        print "sync google contacts"
