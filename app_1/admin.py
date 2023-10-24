from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Korisnik
# Register your models here.

@admin.register(Korisnik)
class KorisnikAdmin(UserAdmin):
    list_display = ['username','status', 'role']
    fieldsets = UserAdmin.fieldsets + (
        ('None', {'fields':('status','role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + ( 
        ('None', {'fields':('status','role')}),
    )
