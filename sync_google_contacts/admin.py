#!/usr/bin/env python

from django.contrib import admin
from django.db import models
from sync_google_contacts.models import GoogleAdminAccounts
from sync_google_contacts.models import PhoneNumber

class googleadminaccountAdmin(admin.ModelAdmin):
    pass

class phonenumberAdmin(admin.ModelAdmin):
    pass

admin.site.register(GoogleAdminAccounts, googleadminaccountAdmin)
admin.site.register(PhoneNumber, phonenumberAdmin)
