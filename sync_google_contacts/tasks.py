#!/usr/bin/env python

from datetime import timedelta
import datetime
import time
import pprint

from pygeocoder import Geocoder
import phonenumbers

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from celery.task import PeriodicTask

if __name__ != "__main__":
    from models import GoogleAdminAccounts
import gdata.contacts.client as gdc

contacts = []
allgroups = []

def replace_none(node):
    '''
    replaces all none items by empty string
    '''
    for key, item in node.items():
        if hasattr(item, '__iter__'):
            node = replace_none(item)
        else:
            #It is a leaf
            if node[key] == None : node[key] = ""
    return node

def gather_contacts(email, password):
    global contacts
    global allgroups

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
                print '----'
                for rec in group_mem :
                    print rec.__dict__
                #print entry.__dict__
                change_date = time.strptime(entry.updated.text,  "%Y-%m-%dT%H:%M:%S.%fZ")
                django_change_date = datetime.datetime.fromtimestamp(time.mktime(change_date))
                print 'djd:',django_change_date
                contact['last_changed'] = django_change_date

                contact['phones'] = []
                recs =  entry.phone_number
                for rec in recs:
                    print rec.__dict__
                    pn = rec.uri.replace('tel:','')
                    ppn =  phonenumbers.parse(pn, None)
                    contact['phones'].append(ppn)

                contact['addresses'] = []
                recs = entry.structured_postal_address
                for rec in recs:
                    addr = rec.formatted_address.text
                    gaddr = Geocoder.geocode(addr)
                    contact['addresses'].append(gaddr)

                print '----'
                contact['family_name'] = ''
                contact['given_name'] = ''
                if entry.name != None :
                    #print entry.name.__dict__
                    if entry.name.family_name != None : contact['family_name'] = entry.name.family_name.text
                    if entry.name.given_name != None : contact['given_name'] = entry.name.given_name.text
                for rec in entry.email:
                    #print rec
                    if rec.primary == 'true' :
                        email = rec.address
                        group_list = []
                        for g in  group_mem:
                            if groups.has_key(g.href) :
                                group_list.append(groups[g.href])
                                allgroups.append(groups[g.href])
                        contact['email'] = email
                        contact['groups'] = group_list
                        contacts.append(contact)

                #print entry.email[0].__dict__
            #print email
    print "results"
    pp = pprint.PrettyPrinter(depth=6)
    pp.pprint(contacts)
    allgroups = list(set(allgroups))
    print allgroups

def write_contacts():
    global contacts
    global allgroups

    for group in allgroups :
        grp = None
        try:
            grp = Group.objects.get(name=group)
        except :
            pass
        if not grp :
            grp = Group()
            grp.name = group
            grp.save()

    for contact in contacts :
        user = None
        try:
            user = User.objects.get(username=contact['email'])
        except :
            pass
        if not user :
            user = User()
            user.username = contact['email']
            user.email = contact['email']
            user.is_active = False
            user.last_name = contact['family_name']
            user.first_name = contact['given_name']
            user.save()
            for grp in contact['groups']:
                g = Group.objects.get(name=grp)
                g.user_set.add(user)

            user.save()


class pull_contacts_from_google(PeriodicTask):
    run_every = timedelta(seconds=15)

    def run(self, **kwargs):
        global contacts
        global allgroups

        contacts = []
        allgroups = []
        #print "sync google contacts"
        admin_accounts = GoogleAdminAccounts.objects.filter(enable=True).order_by('priority').reverse()
        if len(admin_accounts) > 0 :
            account = admin_accounts[0]
            gather_contacts(account.email, account.password)
            write_contacts()

if __name__ == "__main__":
    gather_contacts('sprengee54@gmail.com','quinn2004')
