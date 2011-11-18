# -*- coding: utf-8 -*-

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
        # Create object to serialize
        transaction_output = []
        for transaction in self.related_transactions:
            transaction_output.append({
                'id': transaction.id,    
                'description': transaction.description,
                'title': transaction.title,
                'transaction_type': transaction.transaction_type,
                'created_date': str(transaction.created_date),
                'recipient': transaction.recipient.id,
                'sender': transaction.sender.id,
            })
        # Serialize to JSON
        content = simplejson.dumps({
               'related_transactions': transaction_output
        })

        return content

    def dispatch(self, request, *args, **kwargs):
        return super(TransactionListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.transactions_sent = self.request.user.transactions_sent.all()
        self.transactions_received = self.request.user.transactions_received.all()
        self.related_transactions = self.transactions_sent | self.transactions_received

        return self.related_transactions

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TransactionListView, self).get_context_data(**kwargs)

        debt_to_collect = 0
        debt_to_pay = 0

        # Tentative logic to calculate balances
        # Calculate debt to collect
        for transaction in self.transactions_sent.iterator():
                amount = transaction.latest_revision().amount
                transaction_type = transaction.transaction_type;
                if transaction_type == 'D':
                    if amount >= 0:
                        debt_to_collect += amount
                    else:
                        debt_to_pay += amount
                elif transaction_type == 'P':
                    if amount >= 0:
                        debt_to_pay -= amount
                    else:
                        debt_to_collect -= amount

        # Calculate debt to pay
        for transaction in self.transactions_received.iterator():
                amount = transaction.latest_revision().amount
                if transaction_type == 'D':
                    if amount >= 0:
                        debt_to_collect -= amount
                    else:
                        debt_to_pay -= amount
                elif transaction_type == 'P':
                    if amount >= 0:
                        debt_to_pay += amount
                    else:
                        debt_to_collect += amount

        context['debt_to_collect'] = debt_to_collect
        context['debt_to_pay'] = debt_to_pay

        return context


class TransactionCreateView(CreateView):
    """
    Transaction Create View
    """
    def dispatch(self, request, *args, **kwargs):
        context = {}

        if request.method == 'POST':
            form = TransactionCreateForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                recipient_email = form.cleaned_data['recipient_email']
                transaction_type = form.cleaned_data['transaction_type']
                amount = form.cleaned_data['amount']

                recipient = User.objects.filter(email__iexact=recipient_email)[0]

                new_transaction = Transaction(sender=request.user, recipient=recipient, title=title, description=description, transaction_type=transaction_type)
                new_transaction.save()
                new_revision = TransactionRevision(transaction=new_transaction, amount=amount, status='P', comment='')
                new_revision.save()

                # Redirect
                return redirect('transaction_list_view')

        form = context['form'] = TransactionCreateForm()

        return render_to_response('tracker/transaction_create.html', context, context_instance=RequestContext(request))



class TransactionRevisionListView(ListView):
    """
    List of revisions of a transaction
    """

    context_object_name = "transaction_revision_list"
    template_name = "tracker/transaction_revision_list.html"

    def dispatch(self, request, *args, **kwargs):
        return super(TransactionRevisionListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.transaction = get_object_or_404(Transaction, id__exact=self.kwargs['transaction_id'])
        self.transaction_revisions = self.transaction.revisions.all()

        return self.transaction_revisions

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TransactionRevisionListView, self).get_context_data(**kwargs)
        context['transaction'] = self.transaction

        return context

class TransactionRevisionCreateView(CreateView):
    """
    Transaction Revision Create View

    Edit a transaction (by adding a revision)
    """
    def dispatch(self, request, *args, **kwargs):
        context = {}

        transaction = get_object_or_404(Transaction, id__exact=kwargs['transaction_id'])
        if (transaction.sender != request.user and transaction.recipient != request.user):
            return render_to_response('not_authorized.html', context, context_instance=RequestContext(request))

        if request.method == 'POST':
            form = TransactionRevisionCreateForm(request.POST)
            if form.is_valid():
                comment = form.cleaned_data['comment']
                amount = form.cleaned_data['amount']
                
                new_revision = TransactionRevision(transaction=transaction, amount=amount, status='P', comment=comment)
                new_revision.save()

                # Redirect
                return redirect('transaction_list_view')

        form = context['form'] = TransactionRevisionCreateForm()

        return render_to_response('tracker/transaction_revision_create.html', context, context_instance=RequestContext(request))
