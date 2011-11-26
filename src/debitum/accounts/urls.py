from django.contrib.auth import views as auth_views
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('',
    # Examples:

    # registration
    url(r'^register/$', 'accounts.views.register', {}, name='account_register'),
    url(r'^register/ajax/$', 'accounts.views.registerajax', {}, name='account_register'),
    url(r'^register/success/', direct_to_template, {'template': 'accounts/register_success.html'}, name='account_register_success'),

    # activation
    url(r'^activate/success/$', direct_to_template, {'template': 'accounts/activate_success.html'}, name='account_activate_success'),
    url(r'^activate/(?P<activation_key>\w+)/$', 'accounts.views.activate', {}, name='account_activate'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='account_login' ),
    url(r'^login/ajax/$',  'accounts.views.loginajax'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='account_logout'),
    
    url(r'^profile/(?P<username>\w+)/$', 'accounts.views.profile', {}, name='account_profile'),
    url(r'^profile/$', 'accounts.views.profile', {}, name='account_profile'),
)
