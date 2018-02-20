from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ReliefEffortForm, ItemRequestForm, LoginForm, OrgAdminSignUpForm, DonorSignUpForm
from .models import ReliefEffort, ItemRequest, User, OrgAdmin, Donor
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView

# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def relief_efforts_index(request):
    relief_efforts = ReliefEffort.objects.all()
    return render(request, 'relief-efforts-index.html', {'relief_efforts': relief_efforts})

def show(request, relief_effort_id):
    relief_effort = ReliefEffort.objects.get(id=relief_effort_id)
    current_needs = ItemRequest.objects.filter(relief_effort_id=relief_effort, is_fulfilled=False)
    needs_fulfilled = ItemRequest.objects.filter(relief_effort_id=relief_effort, is_fulfilled=True)
    form = ItemRequestForm()
    return render(request, 'specific-relief.html', {'relief_effort':relief_effort, 'form': form, 'current_needs': current_needs,'needs_fulfilled':needs_fulfilled})

def show_donor_profile(request, user_id):
    user = User.objects.get(id=user_id)
    donor = Donor.objects.filter(user=user)
    return render(request, 'donor_profile.html', {'user': user, 'donor': donor})

def show_org_admin_profile(request, user_id):
    user = User.objects.get(id=user_id)
    org_admin = OrgAdmin.objects.get(user=user)
    relief_efforts = ReliefEffort.objects.filter(org_admin_id=org_admin)
    form = ReliefEffortForm()
    return render(request, 'org_admin_profile.html', {'user': user, 'org_admin': org_admin, 'form': form, 'user_id':user_id, 'relief_efforts':relief_efforts})

def post_relief_effort(request):
    form = ReliefEffortForm(request.POST)
    org_admin = OrgAdmin.objects.get(user=request.user)
    if form.is_valid():
        relief_effort = ReliefEffort(
            name=form.cleaned_data['name'],
            desc=form.cleaned_data['desc'],
            location=form.cleaned_data['location']
        )
        relief_effort.org_admin_id = org_admin
        relief_effort.save()
        path = '/' + str(request.user.id) + '/org-admin-profile/'
    return HttpResponseRedirect(path)

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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def signup(request):
    return render(request, 'signup.html')

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

def post_donate(request):
    item_request_id = request.GET.get('item_request_id', None)
    item_request = ItemRequest.objects.get(id=item_request_id)
    item_request.is_fulfilled = True
    item_request.save()
    return HttpResponse("Fulfilled")
