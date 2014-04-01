#!/usr/bin/env python

from datetime import timedelta
import datetime
import time
import pprint
import pytz

from pygeocoder import Geocoder
import phonenumbers

from celery.task import PeriodicTask
from django.utils import timezone

if __name__ != "__main__":
    from django.contrib.auth.models import User
    from django.contrib.auth.models import Group
    from models import GoogleAdminAccounts
    from models import PhoneNumber
import gdata.contacts.client as gdc

tel_types = ['mobile', 'work', 'home', 'main', 'work_fax', 'home_fax']
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
                change_date = time.strptime(entry.updated.text,  "%Y-%m-%dT%H:%M:%S.%fZ")
                django_change_date = datetime.datetime.fromtimestamp(time.mktime(change_date))
                #print 'djd:',django_change_date
                contact['last_changed'] = django_change_date

                contact['phones'] = []
                recs =  entry.phone_number
                for rec in recs:
                    if rec.uri != None :
                        #print rec.__dict__
                        pdict = {}

                        pn = rec.uri.replace('tel:','')
                        ppn =  phonenumbers.parse(pn, None)
                        pdict['tel'] = ppn
                        pdict['type'] = rec.rel
                        contact['phones'].append(pdict)

                contact['addresses'] = []
                recs = entry.structured_postal_address
                for rec in recs:
                    addr = rec.formatted_address.text
                    gaddr = Geocoder.geocode(addr)
                    contact['addresses'].append(gaddr)

                contact['family_name'] = ''
                contact['given_name'] = ''
                if entry.name != None :
                    if entry.name.family_name != None : contact['family_name'] = entry.name.family_name.text
                    if entry.name.given_name != None : contact['given_name'] = entry.name.given_name.text
                for rec in entry.email:
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

        user = User.objects.get(email='a@a.be')
        contacts = []
        allgroups = []
        #print "sync google contacts"
        admin_accounts = GoogleAdminAccounts.objects.filter(enable=True).order_by('priority').reverse()
        if len(admin_accounts) > 0 :
            account = admin_accounts[0]
            gather_contacts(account.email, account.password)
            write_contacts()
            for contact in contacts:
                t = timezone.now() # offset-awared datetime
                now_aware = contact['last_changed'].replace(tzinfo=pytz.UTC)
                #t.astimezone(timezone.utc).replace(tzinfo=None)
                #print now_aware < account.last_changed
                if len(contact['phones']) > 0 :
                    p = PhoneNumber()
                    p.user = user
                    pn = phonenumbers.format_number(contact['phones'][0]['tel'], phonenumbers.PhoneNumberFormat.E164)
                    found_type = ""
                    for tel_type in tel_types:
                        if tel_type in contact['phones'][0]['type'] :
                            found_type = tel_type

                    #found = any(contact['phones'][0]['type'] in item for item in tel_types)
                    print 'fnd:', found_type
                    p.phone_type = found_type
                    p.phone_number = pn
                    p.save()
            account.last_changed = t
            account.save()

if __name__ == "__main__":
    gather_contacts('sprengee54@gmail.com','quinn2004')
