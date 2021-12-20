from django import forms
from django.forms.widgets import PasswordInput

class loginfrom(forms.Form):
    username = forms.CharField(label='Username', max_length=50, required=True)
    passwd = forms.CharField(label='Password',max_length=50,required=True,widget=PasswordInput())