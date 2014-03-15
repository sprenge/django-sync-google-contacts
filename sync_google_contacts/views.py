# Create your views here.
import time
import os
import re
from datetime import datetime

from django.utils import timezone
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.core.context_processors import csrf
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from models import GoogleAdminAccounts
from django.conf import settings

#1. Test if Permission is granted
#--------------------------------

def user_has_access(request):
    '''
    Has current user user permission to change the groups/users ?
    '''
    user_query = User.objects.filter(username=str(request.user))
    perms = []
    if len(user_query) > 0 :
        perms = user_query[0].get_all_permissions()

    for perm in perms:
        if perm.find('change_user') > 0 :
            return True

    return False

#2. manage google accounts
#-------------------------

def update_google_accounts(request):
    '''
    Main function for managing groups and the attached users
    '''

    if not user_has_access(request) :
        raise Http404

    templ = "update_google_admin_accounts.html"
    try :
        templ = settings.GOOGLE_ADMIN_ACCOUNT_TEMPLATE
    except :
        pass

    return render(request, templ, {  }, context_instance=RequestContext(request))


@csrf_exempt
def ajax_google_account_display(request):
    '''
    display all google accounts
    '''
    if not user_has_access(request) :
        return False

    response_dict = {}
    response_dict['Result'] = 'OK'
    response_dict['Records'] = []

    admin_query_all = GoogleAdminAccounts.objects.all()

    for admin in admin_query_all :
        adict = {}
        adict['Id'] = int(admin.id)
        adict['email'] = admin.email
        adict['password'] = admin.password
        adict['priority'] = admin.priority
        response_dict['Records'].append(adict)

    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')

@csrf_exempt
def ajax_google_account_update(request):
    if not user_has_access(request) :
        return False

    response_dict = {}
    response_dict['Result'] = 'OK'
    response_dict['Records'] = []


    argsDict = dict(request.POST.iterlists())
    argsDict = request.POST.dict()

    adict = argsDict
    admin = GoogleAdminAccounts.objects.get(id=int(adict['Id']))
    admin.email = adict['email']
    admin.password = adict['password']
    admin.priority = adict['priority']
    admin.save()
    response_dict['Records'].append(adict)

    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')

@csrf_exempt
def ajax_google_account_add(request):
    print "add called"
    if not user_has_access(request) :
        return False
    print "x"
    response_dict = {}
    response_dict['Result'] = 'OK'

    argsDict = dict(request.POST.iterlists())
    argsDict = request.POST.dict()
    adict= argsDict

    already_there = True
    try:
        admin = GoogleAdminAccounts.objects.get(email=adict['email'])
    except Exception:
        already_there = False

    if already_there :
        response_dict['Result'] = 'ERROR'
        response_dict['Message'] = 'Account already exists in table'
    else :
        admin = GoogleAdminAccounts()
        admin.email = adict['email']
        admin.password = adict['password']
        admin.priority = int(adict['priority'])
        admin.save()
        adict['Id'] = admin.id
        print adict
        response_dict['Record'] = adict

    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')

@csrf_exempt
def ajax_google_account_delete(request):
    if not user_has_access(request) :
        return False

    response_dict = {}
    response_dict['Result'] = 'OK'
    response_dict['Records'] = []

    argsDict = dict(request.POST.iterlists())
    argsDict = request.POST.dict()

    adict = argsDict
    admin = GoogleAdminAccounts.objects.get(id=int(adict['Id']))
    admin.delete()

    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')


