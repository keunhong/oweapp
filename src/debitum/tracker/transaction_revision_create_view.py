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

class TransactionRevisionCreateView(CreateView):
    """
    Transaction Revision Create View

    Edit a transaction (by adding a revision)
    """

    def json_serialize(self, revision):
        # Create object to serialize
        transaction_output = {
            'sender': revision.transaction.sender.id,
            'recipient': revision.transaction.recipient.id,
            'created_date': str(revision.transaction.created_date),
            'title': revision.transaction.title,
            'description': revision.transaction.description,
            'type': revision.transaction.transaction_type,
        }
        revision_output = {
            'id': revision.id,
            'amount': revision.amount,
            'created_date': str(revision.created_date),
            'comment': revision.comment,
            'status': revision.status,
        }
        # Serialize to JSON
        content = simplejson.dumps({
                'transaction': transaction_output,
                'revision': revision_output,
        })

        return content

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
                #return redirect('transaction_list_view')
                return HttpResponse(self.json_serialize(new_revision), content_type='application/json')

        form = context['form'] = TransactionRevisionCreateForm()

        return render_to_response('tracker/transaction_revision_create.html', context, context_instance=RequestContext(request))
