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

@csrf_protect
@never_cache
def loginajax(request):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Heavier security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()


            login_output = {
                'status': True,
                'redirect_to': redirect_to,
            }
            return HttpResponse(simplejson.dumps(login_output))
        else:
            login_output = {
                'status': False,
                'error': "Could not find matching user.",
            }
            return HttpResponse(simplejson.dumps(login_output))
    else:
            #return HttpResponse("not ajax")
            form = AuthenticationForm(request, label_suffix='')
            return render_to_response('accounts/login.html', { 'form': form, }, context_instance=RequestContext(request))
