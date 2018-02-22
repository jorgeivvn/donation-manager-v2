from django import forms
from .models import ReliefEffort, User, ItemRequest, OrgAdmin, Donor
from django.db import transaction
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic.edit import UpdateView

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

class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Re-type Password"),
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email","first_name","last_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class OrgAdminSignUpForm(UserCreationForm):
    org_name = forms.CharField(label='Organization Name', max_length=100)
    org_location = forms.CharField(label='Organization Location', max_length=100)
    org_bio = forms.CharField(label='Organization Bio', max_length=300)
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_org_admin = True
        user.save()
        org_admin = OrgAdmin.objects.create(user=user)
        org_admin.org_name = self.cleaned_data.get('org_name')
        org_admin.org_location = self.cleaned_data.get('org_location')
        org_admin.org_bio = self.cleaned_data.get('org_bio')
        org_admin.save()
        return user


class DonorSignUpForm(UserCreationForm):
    location = forms.CharField(max_length=100)
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_donor = True
        user.save()
        donor = Donor.objects.create(user=user)
        donor.location = self.cleaned_data['location']
        donor.save()
        return user
