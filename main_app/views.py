from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ReliefEffortForm, ItemRequestForm, LoginForm
from .models import ReliefEffort, ItemRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    return render(request, 'index.html')

def relief_efforts_index(request):
    relief_efforts = ReliefEffort.objects.all()
    form = ReliefEffortForm()
    return render(request, 'relief-efforts-index.html', {'relief_efforts': relief_efforts, 'form': form})

def show(request, relief_effort_id):
    relief_effort = ReliefEffort.objects.get(id=relief_effort_id)
    ir = ItemRequest.objects.filter(relief_effort_id=relief_effort)
    form = ItemRequestForm()
    return render(request, 'specific-relief.html', {'relief_effort':relief_effort, 'form': form, 'ir':ir})

def post_relief_effort(request):
    form = ReliefEffortForm(request.POST)
    if form.is_valid():
        relief_effort = ReliefEffort(
            name=form.cleaned_data['name'],
            desc=form.cleaned_data['desc'],
            location=form.cleaned_data['location']
        )
        relief_effort.save()
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        # if post, then authenticate (user submitted username and password)
        form = LoginForm(request.POST)
        if form.is_valid():
            e = form.cleaned_data['email']
            p = form.cleaned_data['password']
            user = authenticate(email = e, password = p)
            if user is not None:
                if user. is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The account has been disabled.")
            else:
                print("The email and/or password is incorrect.")
    else:
        form = LoginForm()
        return render(request, 'signup-login.html', {'form': form})

def post_item_request(request, relief_effort_id):
    form = ItemRequestForm(request.POST)
    relief_effort = ReliefEffort.objects.get(id=relief_effort_id)
    if form.is_valid():
        item_request = ItemRequest(
            name=form.cleaned_data['name'],
            desc=form.cleaned_data['desc']
        )
        item_request.relief_effort_id = relief_effort
        item_request.save()
        path = '/' + str(relief_effort_id) + '/'
    return HttpResponseRedirect(path)
