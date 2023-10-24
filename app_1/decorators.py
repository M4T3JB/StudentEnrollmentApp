from django.core.exceptions import PermissionDenied
from .models import Korisnik

def admin_required(function):
    def wrap(request, *args, **kwargs):
        korisnik = Korisnik.objects.get(pk=request.user.pk)
        if korisnik.role == 'adm' and korisnik.is_authenticated and korisnik.is_active:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def professor_required(function):
    def wrap(request, *args, **kwargs):
        korisnik = Korisnik.objects.get(pk=request.user.pk)
        if korisnik.role == 'prof' and korisnik.is_authenticated and korisnik.is_active:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def admin_professor_required(function):
    def wrap(request, *args, **kwargs):
        korisnik = Korisnik.objects.get(pk=request.user.pk)
        if (korisnik.role == 'adm' or korisnik.role == 'prof') and korisnik.is_authenticated and korisnik.is_active:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def admin_student_required(function):
    def wrap(request, *args, **kwargs):
        korisnik = Korisnik.objects.get(pk=request.user.pk)
        if (korisnik.role == 'adm' or korisnik.role == 'stu') and korisnik.is_authenticated and korisnik.is_active:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def student_required(function):
    def wrap(request, *args, **kwargs):
        korisnik = Korisnik.objects.get(pk=request.user.pk)
        if  korisnik.role == 'stu' and korisnik.is_authenticated and korisnik.is_active:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap