#!/usr/bin/env python

from datetime import timedelta
from celery.task import PeriodicTask
if __name__ != "__main__":
    from models import GoogleAdminAccounts
import gdata.contacts.client as gdc

contacts = []

def gather_contacts(email, password):
    global contacts

    gd_client = gdc.ContactsClient()
    gd_client.ClientLogin(email, password, gd_client.source)

    #get groups
    groups = {}
    system_groups = {}

    query = gdc.ContactsQuery(max_results=10000)
    feed = gd_client.GetGroups(q=query)
    if feed:
        for entry in feed.entry:
            if entry.system_group == None :
                groups[entry.id.text] = entry.content.text
            else :
                system_groups[entry.id.text] = entry.content.text.replace('System Group: ','')

    #get contacts
    query = gdc.ContactsQuery(max_results=10000)
    feed = gd_client.GetContacts(q=query)
    if feed:
        for entry in feed.entry:
            group_mem = entry.group_membership_info
            email = ''
            if group_mem :
                contact = {}
                #print '----'
                #print entry.updated.__dict__
                if entry.name != None :
                    #print entry.name.__dict__
                    if entry.name.family_name != None : contact['family_name'] = entry.name.family_name.text
                    if entry.name.given_name != None : contact['given_name'] = entry.name.given_name.text
                for rec in entry.email:
                    #print rec
                    if rec.primary == 'true' :
                        email = rec.address
                        #print email
                        group_list = []
                        for g in  group_mem:
                            if groups.has_key(g.href) :
                                group_list.append(groups[g.href])
                        contact['email'] = email
                        contact['groups'] = group_list
                        contacts.append(contact)

                #print entry.email[0].__dict__
            #print email
    print contacts

class pull_contacts_from_google(PeriodicTask):
    run_every = timedelta(seconds=15)

    def run(self, **kwargs):
        global contacts

        contacts = []
        #print "sync google contacts"
        admin_accounts = GoogleAdminAccounts.objects.filter(enable=True).order_by('priority').reverse()
        for account in admin_accounts :
            gd_client = gdc.ContactsClient()
            gd_client.ClientLogin(account.email, account.password, gd_client.source)

            #get contacts
            query = gdc.ContactsQuery(max_results=10000)
            feed = gd_client.GetContacts(q=query)
            if feed:
                for entry in feed.entry:
                    print entry

            #get groups
            query = gdc.ContactsQuery(max_results=10000)
            feed = gd_client.GetGroups(q=query)
            if feed:
                for entry in feed.entry:
                    print entry

if __name__ == "__main__":
    gather_contacts('sprengee54@gmail.com','quinn2004')
