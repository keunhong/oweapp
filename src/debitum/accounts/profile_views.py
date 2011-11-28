# -*- coding: utf-8 -*-

import urlparse
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import *
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

from django.utils import simplejson

from forms import *
from models import *
import hashlib

def profile(request, username=None):
    """
    Activate User
    """
    if not request.user.is_authenticated():
        output = {
            'status': False,
            'error': "Not logged in",
        }
        return HttpResponse(simplejson.dumps(output))

    # User queried for
    if username is None:
        query_user = request.user
    else:
        query_user = User.objects.get(username=username)

    if query_user is None:
        output = {
            'status': False,
            'error': "Unknown user",
        }
        return HttpResponse(simplejson.dumps(output))



    if request.GET.get('format','html') == 'json':
        content = simplejson.dumps({
            'status': True,
            'id': query_user.id,
            'email': query_user.email,
            'first_name': query_user.first_name,
            'last_name': query_user.last_name,
        })
        return HttpResponse(content)
    else:
        request.session['query_user'] = query_user
        return render_to_response('accounts/profile.html', { 'query_user': query_user, }, context_instance=RequestContext(request))
