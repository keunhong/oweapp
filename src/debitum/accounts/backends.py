from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import email_re
from django.contrib.auth.backends import ModelBackend

class AccountAuthBackend(ModelBackend):
    """
    AccountAuthBackend

    The default backend for authenticating with an email and password.
    This is the one used for logging in from a normal login page.
    """
    def authenticate(self, username=None, password=None):
        if email_re.search(username):
            try:
                user = User.objects.get(email=username)
                # Check the password is correct for user
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class ActivationAuthBackend(ModelBackend):
    """
    ActivationAuthBackend

    This is the backend used to automatically log in people after
    activating their accounts.
    Gets the user and logs in without checking password. Careful!
    """
    def authenticate(self, username=None):
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
