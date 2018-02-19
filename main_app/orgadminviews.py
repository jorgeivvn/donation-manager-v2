from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView
from .forms import OrgAdminSignUpForm
from .models import User, OrgAdmin
from django.contrib.auth import login

class OrgAdminSignUpView(CreateView):
    model = User
    form_class = OrgAdminSignUpForm
    template_name = 'org-admin-signup-v2.html'

    def get_context_data(self, **kwargs):
        # kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')
