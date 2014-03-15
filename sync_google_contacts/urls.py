import sys

from django.conf.urls import patterns, include, url
from django.conf.urls import patterns, url

from sync_google_contacts.views import update_google_accounts
from sync_google_contacts.views import ajax_google_account_add
from sync_google_contacts.views import ajax_google_account_delete
from sync_google_contacts.views import ajax_google_account_display
from sync_google_contacts.views import ajax_google_account_update

urlpatterns = patterns('',
    #
    url(r'^update/$', update_google_accounts, name='update_google_accounts'),
    url(r'^ajax/google-accounts/display/$', ajax_google_account_display),
    url(r'^ajax/google-accounts/update/$', ajax_google_account_update),
    url(r'^ajax/google-accounts/delete/$', ajax_google_account_delete),
    url(r'^ajax/google-accounts/add/$', ajax_google_account_add),


)

