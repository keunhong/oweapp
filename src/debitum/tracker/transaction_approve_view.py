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

class TransactionApproveView(CreateView):
    """
    Transaction Revision Create View

    Edit a transaction (by adding a revision)
    """
    def dispatch(self, request, *args, **kwargs):
        context = {}

        # User must be recipient of transaction to approve
        if request.method == 'POST':
            form = TransactionApproveForm(request.POST)

            if form.is_valid():
                transaction = get_object_or_404(Transaction, id__exact=form.cleaned_data['transaction_id'])
                revision = transaction.latest_revision()
                # Check whether related to transaction at all
                if transaction.recipient != request.user and transaction.sender != request.user:
                    return HttpResponse(simplejson.dumps({'status': False, 'error': "Not related"}))

                # Only the opposite party can approve
                if revision.author == request.user:
                    return HttpResponse(simplejson.dumps({'status': False, 'error': "Cannot approve own revision"}))

                # Actually approve and save
                revision.status = 'A'
                revision.save()

                return HttpResponse(simplejson.dumps({'status': True}))

        form = context['form'] = TransactionApproveForm()

        return render_to_response('tracker/transaction_revision_create.html', context, context_instance=RequestContext(request))
