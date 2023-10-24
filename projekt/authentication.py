from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from app_1.models import Korisnik

class  SettingsBackend(object):

    def authenticate(self, username=None, password=None):
        try:
            user = Korisnik.objects.get(username=username)
        except:
            return None
        pwd_valid = check_password(password, user.password)
        if username and pwd_valid:
            user = Korisnik.objects.get(username=username)
            return user
        return None
    
    def check_user_name(self, name):
        try:
            Korisnik.objects.get(username=name)
        except:
            return None
        raise ValidationError("Username taken")
    
    def checkPasswords(self, user, password1=None, password2=None):
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        else:
            user.set_password(password1)
        return user
    
  