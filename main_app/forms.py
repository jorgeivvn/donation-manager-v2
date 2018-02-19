from django import forms
from .models import ReliefEffort
from .models import ItemRequest

class ReliefEffortForm(forms.ModelForm):
    class Meta:
        model = ReliefEffort
        fields = ['name','desc','location']


class ItemRequestForm(forms.ModelForm):
    class Meta:
        model = ItemRequest
        fields = ['name','desc']

class LoginForm(forms.Form):
    email = forms.CharField(label="Email", max_length=254)
    password = forms.CharField(widget=forms.PasswordInput())
