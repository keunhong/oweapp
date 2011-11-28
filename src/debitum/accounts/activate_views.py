# -*- coding: utf-8 -*-

import urlparse
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import *
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

from django.utils import simplejson

from forms import *
from models import *

def activate(request, activation_key):
    """
    Activate User
    """
    user = RegistrationProfile.objects.activate_account(activation_key)

    if user is None:
        raise Http404

    # Autologin user
    # The login function requires user.backend.
    from django.contrib.auth import authenticate, login
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    request.session['user'] = user
    output = {
        'status': True,
    }
    return HttpResponse(simplejson.dumps(output))
    #return redirect('account_activate_success');
