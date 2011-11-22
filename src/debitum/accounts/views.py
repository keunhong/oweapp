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
            }
            return HttpResponse(simplejson.dumps(login_output))
    else:
            #return HttpResponse("not ajax")
            form = AuthenticationForm(request, label_suffix='')
            return render_to_response('accounts/login.html', { 'form': form, }, context_instance=RequestContext(request))


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

def profile(request, username=None):
    """
    Activate User
    """
    if not request.user.is_authenticated():
        context = {}
        context['error_title'] = _(u"Not authorized")
        context['error_body'] = _(u"You do not have the permissions to access this page.")
        return render_to_response('error.html', context, context_instance=RequestContext(request))

    # User queried for
    if username is None:
        query_user = request.user
    else:
        query_user = User.objects.get(username=username)

    if query_user is None:
        raise Http404



    if request.GET.get('format','html') == 'json':
        content = simplejson.dumps({
            'id': query_user.id,
            'email': query_user.email,
            'first_name': query_user.first_name,
            'last_name': query_user.last_name,
        })
        return HttpResponse(content)
    else:
        request.session['query_user'] = query_user
        return render_to_response('accounts/profile.html', { 'query_user': query_user, }, context_instance=RequestContext(request))
