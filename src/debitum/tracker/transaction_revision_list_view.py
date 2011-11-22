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

class TransactionRevisionListView(ListView):
    """
    List of revisions of a transaction
    """

    context_object_name = "transaction_revision_list"
    template_name = "tracker/transaction_revision_list.html"

    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format','html') == 'json':
            return HttpResponse(self.json_serialize(), content_type='application/json')
        else:
            return ListView.render_to_response(self, context)

    def json_serialize(self):
        # Create object to serialize
        transaction_output = {
            'sender': self.transaction.sender.id,
            'recipient': self.transaction.recipient.id,
            'created_date': str(self.transaction.created_date),
            'title': self.transaction.title,
            'description': self.transaction.description,
            'type': self.transaction.transaction_type,
        }
        revision_output = []
        for revision in self.transaction_revisions:
            revision_output.append({
                'id': revision.id,
                'amount': revision.amount,
                'created_date': str(revision.created_date),
                'comment': revision.comment,
                'status': revision.status,
            })
        # Serialize to JSON
        content = simplejson.dumps({
                'transaction': transaction_output,
                'revisions': revision_output,
        })

        return content

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
