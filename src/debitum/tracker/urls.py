from django.contrib.auth import views as auth_views
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from views import *


urlpatterns = patterns('',
    url(r'^transactions/$', login_required(TransactionListView.as_view()), name='transaction_list_view'),
    url(r'^transactions/create/$', login_required(TransactionCreateView.as_view()), name='transaction_create_view'),
    url(r'^transactions/(?P<transaction_id>\d+)/edit/$', login_required(TransactionRevisionCreateView.as_view()), name='transaction_revision_create_view'),
    url(r'^transactions/(?P<transaction_id>\d+)/revisions/$', login_required(TransactionRevisionListView.as_view()), name='transaction_revision_list_view'),

    url(r'^transactions/pending/$', login_required(PendingTransactionListView.as_view()), name='pending_transaction_list_view'),

    url(r'^transactions/approve/$', login_required(TransactionApproveView.as_view()), name='transaction_approve_view'),
)
