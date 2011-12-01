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
from django.core.exceptions import *

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
                'status': True,
                'transaction': transaction_output,
                'revision': revision_output,
        })

        return content

    def dispatch(self, request, *args, **kwargs):
        context = {}

        # Get transaction
        #transaction = get_object_or_404(Transaction, id__exact=kwargs['transaction_id'])
        try:
            transaction = Transaction.objects.get(pk=kwargs['transaction_id'])
        except ObjectDoesNotExist:
            output = {
                'status': False,
                'error': "Does not exist",
            }
            return HttpResponse(simplejson.dumps(output))


        # Check whether user is related to transaction
        if (transaction.sender != request.user and transaction.recipient != request.user):
            output = {
                'status': False,
                'error': "Unauthorized",
            }
            return HttpResponse(simplejson.dumps(output))
            #return render_to_response('not_authorized.html', context, context_instance=RequestContext(request))

        # If post process
        if request.method == 'POST':
            form = TransactionRevisionCreateForm(request.POST)
            if form.is_valid():
                comment = form.cleaned_data['comment']
                amount = form.cleaned_data['amount']
                
                new_revision = TransactionRevision(transaction=transaction, amount=amount, status='P', comment=comment, author=request.user)
                new_revision.save()

                return HttpResponse(self.json_serialize(new_revision), content_type='application/json')

        # If not post render form
        form = context['form'] = TransactionRevisionCreateForm()
        return render_to_response('tracker/transaction_revision_create.html', context, context_instance=RequestContext(request))
