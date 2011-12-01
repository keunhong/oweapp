from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext_lazy as _

# Create your models here.
STATUS_CHOICES = (
    ('P', 'Pending approval'),
    ('A', 'Approved'),
    ('C', 'Canceled'),
)
TYPE_CHOICES = (
    ('D', 'Debt'),
    ('P', 'Payment'),
)
class PendingTransactionManager(models.Manager):
    def get_query_set(self):
        qs = super(PendingTransactionManager, self).get_query_set()
        for q in qs:
            if q.latest_revision().status != 'P':
                q.delete()

        return qs

class Transaction(models.Model):
    """
    Represents a transaction

    Money is going from sender to recipient
    Positive amount means sender sent money to recipient
        If debt: sender lent recipient money
        If payment: sender payed back recipient
    Negative means vice versa
    """

    sender = models.ForeignKey(User, unique=False, verbose_name=_('sender'), related_name = 'transactions_sent')
    recipient = models.ForeignKey(User, unique=False, verbose_name=_('recipient'), related_name = 'transactions_received')

    created_date = models.DateTimeField(_(u"crated date"), auto_now=True)

    title = models.TextField(_(u"title"))
    description = models.TextField(_(u"description"), blank=True)

    transaction_type = models.CharField(max_length=1, choices=TYPE_CHOICES)

    def latest_revision(self):
        """
        Latest Post
        """
        return self.revisions.latest('created_date')

class TransactionRevision(models.Model):
    """
    Represents a revision of a transaction

    One of these is added every time the transaction is edited
    """
    transaction = models.ForeignKey(Transaction, verbose_name=_('parent transaction'), related_name='revisions')

    author = models.ForeignKey(User, unique=False, verbose_name=_('author'), related_name = 'revisions_created')

    created_date = models.DateTimeField(_(u"created date"), auto_now_add=True)

    amount = models.IntegerField(_(u"amount"))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    comment = models.TextField(_(u"comment"), blank=True)
