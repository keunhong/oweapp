from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import Http404
from django.views.generic import *
from django.http import HttpResponse
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from models import *
from forms import *
import json
from django.views.generic.list import *

from django import http
from django.utils import simplejson as json
from django.core import serializers
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

class TransactionListView(ListView):
    """
    View that shows the list of transactions relevant to the logged in user
    """

    context_object_name = "transaction_list"
    template_name = "tracker/transaction_list.html"

    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format','html') == 'json':
            return HttpResponse(self.json_serialize(), content_type='application/json')
        else:
            return ListView.render_to_response(self, context)

    def json_serialize(self):
        # Serialize to JSON
        content = simplejson.dumps(self.people.values())

        return content

    def dispatch(self, request, *args, **kwargs):
        return super(TransactionListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.transactions_sent = self.request.user.transactions_sent.all()
        self.transactions_received = self.request.user.transactions_received.all()
        self.related_transactions = self.transactions_sent | self.transactions_received

        self.people = {}
        for transaction in self.related_transactions:
            # Create entry
            entry = {
                'transactions': [],
            }
            # Create transaction entry
            transaction_entry = {
                'title': transaction.title,
                'description': transaction.description,
                'amount': transaction.latest_revision().amount,
                'date': str(transaction.latest_revision().created_date),
            }
            # If the current user sent the transaction
            if transaction.sender == self.request.user:
                opposite = transaction.recipient
                if not transaction.recipient.id in self.people:
                    self.people[transaction.recipient.id] = entry
                self.people[opposite.id]['transactions'].append(transaction_entry)

            # if the current user received the transaction
            if transaction.recipient == self.request.user:
                opposite = transaction.sender
                transaction_entry['amount'] = transaction_entry['amount'] * -1
                if not transaction.sender.id in self.people:
                    self.people[transaction.sender.id] = entry
                self.people[opposite.id]['transactions'].append(transaction_entry)

            # Add user information
            entry['id'] = opposite.id
            entry['first_name'] = opposite.first_name
            entry['last_name'] = opposite.last_name

            print entry

        return self.related_transactions

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TransactionListView, self).get_context_data(**kwargs)

        return context
