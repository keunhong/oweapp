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

from transaction_list_view import TransactionListView

class TransactionCreateView(CreateView):
    """
    Transaction Create View
    """

    def json_serialize(self, transaction):
        # Create object to serialize
        latest_revision = transaction.latest_revision()
        latest_revision_output = {
            'amount': latest_revision.amount,
            'created_date': str(latest_revision.created_date),
            'comment': latest_revision.comment,
        }
        transaction_output = {
            'id': transaction.id,    
            'description': transaction.description,
            'title': transaction.title,
            'transaction_type': transaction.transaction_type,
            'created_date': str(transaction.created_date),
            'recipient': transaction.recipient.id,
            'sender': transaction.sender.id,
            'latest_revision': latest_revision_output,
        }
        # Serialize to JSON
        content = simplejson.dumps({
               'status': True,
               'transaction': transaction_output
        })

        return content

    def dispatch(self, request, *args, **kwargs):
        context = {}

        if request.method == "POST":
            form = TransactionCreateForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                recipient_email = form.cleaned_data['recipient_email']
                transaction_type = form.cleaned_data['transaction_type']
                amount = form.cleaned_data['amount']

                recipients = User.objects.filter(email__iexact=recipient_email)

                if len(recipients) == 0:
                    output = {
                        'status': False,
                        'error': "Recipient does not exist",
                    }
                    return HttpResponse(simplejson.dumps(output))

                recipient = recipients[0]



                new_transaction = Transaction(sender=request.user, recipient=recipient, title=title, description=description, transaction_type=transaction_type)
                new_transaction.save()
                new_revision = TransactionRevision(transaction=new_transaction, amount=amount, status='P', comment='', author=request.user)
                new_revision.save()

                return HttpResponse(self.json_serialize(new_transaction), content_type='application/json')
            else:
                output = {
                    'status': False,
                    'error': form.errors,
                }
                return HttpResponse(simplejson.dumps(output))
        else:
            # Render form
            form = context['form'] = TransactionCreateForm()
            return render_to_response('tracker/transaction_create.html', context, context_instance=RequestContext(request))
            #output = {
            #    'status': False,
            #    'error': request.method,
            #}
            #return HttpResponse(simplejson.dumps(output))
