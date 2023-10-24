from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from .models import Korisnik, Predmeti
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from .models import Korisnik

class PredmetiForma(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PredmetiForma, self).__init__(*args, **kwargs)
        self.fields.get('nositelj').queryset = Korisnik.objects.filter(role='prof')

    class Meta:
        model = Predmeti
        fields = ['name', 'kod', 'program', 'ects', 'sem_red', 'sem_izv', 'nositelj']
        
    
class AddUserForm(UserCreationForm):  
    username = forms.CharField(label='Korisničko ime', min_length=3, max_length=150, widget=forms.TextInput(attrs={'placeholder': ("Korisničko ime"), 'class': 'reg'} ))
    password1 = forms.CharField(label='Lozinka', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Potvrdi lozinku', widget=forms.PasswordInput)  

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': ("Lozinka"), 'class': 'reg'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': ("Lozinka"), 'class': 'reg'})
        self.fields['role'].widget = forms.HiddenInput()

    class Meta:
        model = Korisnik
        fields = ['username', 'password1', 'password2', 'role', 'status']
    