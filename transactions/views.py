from django.shortcuts import render

from store.views import numOfDays
from .forms import *
from django.shortcuts import render, redirect
from .models import *
from datetime import date


# Create your views here.

def add_inward(request):
    
    
    if request.method == 'POST':

        forms = inward_Form(request.POST)
        DC_date = request.POST.get('DC_date')

        date_time = numOfDays(DC_date)
        updated_request = request.POST.copy()
        updated_request.update({'DC_date': date_time})
        forms = inward_Form(updated_request)

        print(DC_date)

        if forms.is_valid():
            forms.save()
            return redirect('list_inward')
        else:
            print(forms.errors)
    
    else:

        forms = inward_Form()

        context = {
            'form': forms
        }
        return render(request, 'transactions/add_inward.html', context)


def list_inward(request):

    data = inward.objects.all()

    context = {
        'data': data,
    }
    
    return render(request, 'transactions/list_inward.html', context)


def add_outward(request):

    if request.method == 'POST':

        forms = outward_Form(request.POST)
        DC_date = request.POST.get('DC_date')

        date_time = numOfDays(DC_date)
        updated_request = request.POST.copy()
        updated_request.update({'DC_date': date_time})
        forms = outward_Form(updated_request)

        print(DC_date)

        if forms.is_valid():
            forms.save()
            return redirect('list_outward')
        else:
            print(forms.errors)
    
    else:

        forms = outward_Form()

        context = {
            'form': forms
        }
        return render(request, 'transactions/add_outward.html', context)



def list_outward(request):

    data = outward.objects.all()

    context = {
        'data': data,
    }
    
    return render(request, 'transactions/list_outward.html', context)

