from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView
from .forms import OrgAdminSignUpForm
from .models import User, OrgAdmin, ItemRequest
from django.contrib.auth import login

class OrgAdminSignUpView(CreateView):
    model = User
    form_class = OrgAdminSignUpForm
    template_name = 'org-admin-signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        path = '/' + str(user.id) + '/org-admin-profile/'
        return redirect(path)
