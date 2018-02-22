from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ReliefEffortForm, ItemRequestForm, LoginForm, OrgAdminSignUpForm, DonorSignUpForm
from .models import ReliefEffort, ItemRequest, User, OrgAdmin, Donor, Donation
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView

# Create your views here.

def generate_completion_percentages(relief_effort_list):
    percentage_list = [];
    for relief_effort in relief_effort_list:
        current_needs = ItemRequest.objects.filter(relief_effort_id=relief_effort.id, is_fulfilled=False)
        needs_fulfilled = ItemRequest.objects.filter(relief_effort_id=relief_effort.id, is_fulfilled=True)
        if len(current_needs) > 0 or len(needs_fulfilled) > 0:
            percentage_fulfilled = round(((len(needs_fulfilled) / (len(needs_fulfilled) + len(current_needs))) * 100), 2)
        else:
            percentage_fulfilled = 0;
        percentage_and_re = {}
        green = int(255 * percentage_fulfilled / 100)
        red = 255 - green
        percentage_and_re['percentage_fulfilled'] = percentage_fulfilled
        percentage_and_re['relief_effort'] = relief_effort
        percentage_and_re['color'] = 'rgb({},{},50)'.format(red, green)
        percentage_list.append(percentage_and_re)
    return percentage_list


def index(request):
    relief_efforts = ReliefEffort.objects.all()
    if len(relief_efforts) == 1:
        first_article = relief_efforts[len(relief_efforts) - 1]
        return render(request, 'index.html', {'first_article': first_article})
    elif len(relief_efforts) == 2:
        first_article = relief_efforts[len(relief_efforts) - 1]
        second_article = relief_efforts[len(relief_efforts) - 2]
        return render(request, 'index.html', {'first_article': first_article, 'second_article': second_article})
    elif len(relief_efforts) == 3:
        first_article = relief_efforts[len(relief_efforts) - 1]
        second_article = relief_efforts[len(relief_efforts) - 2]
        third_article = relief_efforts[len(relief_efforts) - 3]
        return render(request, 'index.html', {'first_article': first_article, 'second_article': second_article, 'third_article': third_article})
    elif len(relief_efforts) > 3:
        first_article = relief_efforts[len(relief_efforts) - 1]
        second_article = relief_efforts[len(relief_efforts) - 2]
        third_article = relief_efforts[len(relief_efforts) - 3]
        fourth_article = relief_efforts[len(relief_efforts) - 4]
        return render(request, 'index.html', {'first_article': first_article, 'second_article': second_article, 'third_article': third_article, 'fourth_article': fourth_article})
    else:
        return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')

def relief_efforts_index(request):
    relief_efforts = ReliefEffort.objects.all()
    percentage_list = generate_completion_percentages(relief_efforts)
    def get_percentage(item):
        return item['percentage_fulfilled']
    sorted_list = sorted(percentage_list, key=get_percentage)
    return render(request, 'relief-efforts-index.html', {'relief_efforts': relief_efforts, 'sorted_list': sorted_list})

def show(request, relief_effort_id):
    relief_effort = ReliefEffort.objects.get(id=relief_effort_id)
    orgAdmin = str(relief_effort.org_admin_id.user)
    org_admin = OrgAdmin.objects.get(user=relief_effort.org_admin_id.user)
    org_admin_user = User.objects.get(email=org_admin.user)
    if request.user.is_anonymous:
        currentUser = None
    else:
        currentUser = str(request.user.email)
    string_spacer = "%20"
    split_text = relief_effort.name.split(" ")
    tweet_text = string_spacer.join(split_text)
    current_needs = ItemRequest.objects.filter(relief_effort_id=relief_effort, is_fulfilled=False)
    needs_fulfilled = ItemRequest.objects.filter(relief_effort_id=relief_effort, is_fulfilled=True)
    if len(current_needs) > 0 or len(needs_fulfilled) > 0:
        percentage_fulfilled = round(((len(needs_fulfilled) / (len(needs_fulfilled) + len(current_needs))) * 100), 2)
    else:
        percentage_fulfilled = 0;
    form_list = []
    create_form = ItemRequestForm()
    green = int(255 * percentage_fulfilled / 100)
    red = 255 - green
    color = 'rgb({},{},50)'.format(red, green)
    return render(request, 'specific-relief.html', {'relief_effort':relief_effort, 'create_form': create_form, 'current_needs': current_needs,'needs_fulfilled':needs_fulfilled, 'orgAdmin':orgAdmin, 'currentUser':currentUser, 'tweet_text': tweet_text, 'percentage_fulfilled': percentage_fulfilled, 'color': color, 'org_admin':org_admin, 'org_admin_user':org_admin_user})

def show_donor_profile(request, user_id):
    user = User.objects.get(id=user_id)
    donor = Donor.objects.get(user=user)
    donations = Donation.objects.filter(donor_id=donor)
    donation_list = []
    for donation in donations:
        item_request = ItemRequest.objects.get(id=donation.item_request_id.id)
        relief_effort = ReliefEffort.objects.get(id=item_request.relief_effort_id.id)
        donation_info = {}
        donation_info['name'] = item_request.name
        donation_info['desc'] = item_request.desc
        donation_info['date'] = donation.created_at
        donation_info['relief_effort_name'] = relief_effort.name
        donation_info['relief_effort_desc'] = relief_effort.desc
        donation_info['relief_effort_location'] = relief_effort.location
        donation_info['relief_effort_id'] = relief_effort.id
        donation_list.append(donation_info)
    return render(request, 'donor_profile.html', {'user': user, 'donor': donor, 'donation_list': donation_list})

def show_org_admin_profile(request, user_id):
    user = User.objects.get(id=user_id)
    org_admin = OrgAdmin.objects.get(user=user)
    relief_efforts = ReliefEffort.objects.filter(org_admin_id=org_admin)
    form = ReliefEffortForm()
    percentage_list = generate_completion_percentages(relief_efforts)
    if request.user.is_anonymous:
        currentUser = None
    else:
        currentUser = str(request.user.email)
    org_admin_as_str = str(org_admin.user)
    def get_percentage(item):
        return item['percentage_fulfilled']
    sorted_list = sorted(percentage_list, key=get_percentage)
    return render(request, 'org_admin_profile.html', {'user': user, 'org_admin': org_admin, 'form': form, 'user_id':user_id, 'relief_efforts':relief_efforts, 'percentage_list': sorted_list, 'currentUser': currentUser, 'org_admin_as_str': org_admin_as_str})

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

def remove_item_request(request):
    item_request_id = request.GET.get('item_request_id', None)
    item_request = ItemRequest.objects.get(id=item_request_id)
    item_request.delete()
    return HttpResponse('Item deleted')

def update_item_request(request, item_request_id):
    form = ItemRequestForm(request.POST)
    if form.is_valid():
        item_request = ItemRequest.objects.get(id=item_request_id)
        item_request.name = form.cleaned_data['name']
        item_request.desc = form.cleaned_data['desc']
        item_request.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def update_relief_effort(request, relief_effort_id):
    form = ReliefEffortForm(request.POST)
    if form.is_valid():
        relief_effort = ReliefEffort.objects.get(id=relief_effort_id)
        relief_effort.name = form.cleaned_data['name']
        relief_effort.desc = form.cleaned_data['desc']
        relief_effort.location = form.cleaned_data['location']
        relief_effort.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def make_donation(request, item_request_id):
    user_id = request.POST.get('user_id', None)
    user = User.objects.get(id=user_id)
    donor = Donor.objects.get(user=user)
    item_request = ItemRequest.objects.get(id=item_request_id)
    item_request.is_fulfilled = True
    item_request.save()
    donation = Donation.objects.create(donor_id=donor)
    donation.item_request_id = item_request
    donation.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
