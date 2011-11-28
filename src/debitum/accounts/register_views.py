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

def register(request):
    """
    Register View
    """

    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']
                username = hashlib.sha1(email).hexdigest()[:30]

                first_name = form.cleaned_data['first_name'];
                last_name = form.cleaned_data['last_name'];

                # Create new user
                new_user = RegistrationProfile.objects.create_inactive_user(username, email, password, first_name, last_name)
                new_user_profile = UserProfile(user=new_user)
                new_user_profile.save()

                # Create session variable for printing later
                request.session['user'] = new_user
                return redirect('account_register_success')
        else:
            form = RegistrationForm(label_suffix='')
        
        return render_to_response('accounts/register.html', { 'form': form, }, context_instance=RequestContext(request))
    else:
        return redirect('/')

def registerajax(request):
    """
    Register View
    """

    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']
                username = hashlib.sha1(email).hexdigest()[:30]

                first_name = form.cleaned_data['first_name'];
                last_name = form.cleaned_data['last_name'];

                # Create new user
                new_user = RegistrationProfile.objects.create_inactive_user(username, email, password, first_name, last_name)
                new_user_profile = UserProfile(user=new_user)
                new_user_profile.save()

                # Create session variable for printing later
                request.session['user'] = new_user
                register_output = {
                    'status': True,
                    'user': new_user.id,
                }
            else:
                fields = []
                for field in form:
                    errors = [x for x in field.errors]
                    field_errors = {
                        'label': unicode(field.label),
                        'errors': errors,
                    }
                    fields.append(field_errors)

                register_output = {
                    'status': False,
                    'error': "Validation error",
                    'fields': fields,
                }

            return HttpResponse(simplejson.dumps(register_output))
        else:
            form = RegistrationForm(label_suffix='')
        
        return render_to_response('accounts/register.html', { 'form': form, }, context_instance=RequestContext(request))
    else:
        return redirect('/')
