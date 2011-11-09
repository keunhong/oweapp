# coding=UTF-8

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

import hashlib
import random
import datetime

# Create your models here.
class UserProfile(models.Model):
    """
    UserProfile
    """
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))

    def __unicode__(self):
        return self.user.last_name + self.user.first_name


class RegistrationManager(models.Manager):
    """
    RegistrationManager

    Methods:
        activate_account
        create_inactive_user
        create_registration_profile
    """

    def activate_account(self, activation_key):
        """
        Activate Account

        Given an activation key, this function queries the DB to see
        if there is a matching registration profile. If there is, the
        associated user is activated.
        """
        try:
            registration_profile = self.get(activation_key=activation_key)
        except self.model.DoesNotExist:
            return None

        if not registration_profile.is_expired():
            user = registration_profile.user
            user.is_active = True
            user.save()
            registration_profile.delete()
            return user
        else:
            return None
        
    def create_inactive_user(self, username, email, password, first_name=None, last_name=None):
        """
        Creates and inactive user

        Creates inactive user and an associated registration profile
        which contains an activation key. An email is then sent to the 
        user with the key so they can activate their account.
        """

        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()

        registration_profile = self.create_registration_profile(new_user)
        registration_profile.send_activation_email()

        if not registration_profile:
            return None

        return new_user

    def create_registration_profile(self, user):
        """
        Create profile for registration

        Generates a hashed activation key to create a registration profile
        """
        salt = hashlib.sha1(str(random.random())).hexdigest()[:10]
        activation_key = hashlib.sha1(salt + user.username).hexdigest()

        return self.create(user=user, activation_key=activation_key)
    

class RegistrationProfile(models.Model):
    """
    RegistrationProfile

    A profile containing an activation key that is sent to the user. The user
    can then verify his/her email by untering the activation key.

    Methods:
        is_expired
        send_activation_email
    """

    objects = RegistrationManager()

    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    activation_key = models.CharField(_('activation key'), max_length=40)

    def __unicode__(self):
        return self.user.last_name + self.user.first_name + "("+ self.user.email +")"

    def is_expired(self):
        """
        Is the registration profile expired?

        Returns true if the registration profile is expired. This is
        determined using the joined date and ACCOUNT_ACTIVATION_DAYS
        set in settings.py.
        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)

        return (self.user.date_joined + expiration_date <= datetime.datetime.now())

    def send_activation_email(self):
        """
        Send activation email

        Sends an activation email to the user.
        """
        ctx_dict = {
                        'activation_key': self.activation_key,
                        'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                        'user': self.user,
                        'SITE_URL': settings.SITE_URL,
                    }
        subject = render_to_string('accounts/activation_email_subject.txt', ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        
        message = render_to_string('accounts/activation_email_body.html', ctx_dict)

        msg = EmailMultiAlternatives(subject, message, None, [self.user.email])
        msg.attach_alternative(message, "text/html")
        msg.send()
