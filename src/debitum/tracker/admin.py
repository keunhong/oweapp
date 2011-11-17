from django.contrib import admin
from models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class TransactionRevisionInline(admin.StackedInline):
    model = TransactionRevision

class TransactionAdmin(admin.ModelAdmin):
    inlines = [
        TransactionRevisionInline,
    ]
    save_on_top = True
    list_display = ('sender', 'recipient', 'created_date')

admin.site.register(Transaction, TransactionAdmin)

#admin.site.register(TransactionRevision)
