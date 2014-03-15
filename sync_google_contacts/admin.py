#!/usr/bin/env python

from django.contrib import admin
from django.db import models
from sync_google_contacts.models import GoogleAdminAccounts

class googleadminaccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(GoogleAdminAccounts, googleadminaccountAdmin)
