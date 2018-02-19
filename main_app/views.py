from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ReliefEffortForm
from .forms import ItemRequestForm
from .models import ReliefEffort
from .models import ItemRequest


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
