from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView
from .forms import DonorSignUpForm
from .models import User, Donor
from django.contrib.auth import login

class DonorSignUpView(CreateView):
    model = User
    form_class = DonorSignUpForm
    template_name = 'donor-signup-v2.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')
