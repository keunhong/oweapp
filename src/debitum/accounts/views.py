# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from forms import *
from models import *
import hashlib


# Create your views here.

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
    return redirect('account_activate_success');

def profile(request, username):
    """
    Activate User
    """
    if not request.user.is_authenticated():
        context = {}
        context['error_title'] = _(u"Not authorized")
        context['error_body'] = _(u"You do not have the permissions to access this page.")
        return render_to_response('error.html', context, context_instance=RequestContext(request))

    # User queried for
    query_user = User.objects.get(username=username)

    if query_user is None:
        raise Http404

    request.session['query_user'] = query_user
    return render_to_response('accounts/profile.html', { 'query_user': query_user, }, context_instance=RequestContext(request))
