from django.contrib.auth import views as auth_views
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from views import *


urlpatterns = patterns('',
    url(r'^transactions/$', TransactionListView.as_view(), name='transaction_list_view'),
    url(r'^transactions/create/$', TransactionCreateView.as_view(), name='transaction_create_view'),
    url(r'^transactions/(?P<transaction_id>\d+)/edit/$', TransactionRevisionCreateView.as_view(), name='transaction_revision_create_view'),
    url(r'^transactions/(?P<transaction_id>\d+)/revisions/$', TransactionRevisionListView.as_view(), name='transaction_revision_list_view'),
)
