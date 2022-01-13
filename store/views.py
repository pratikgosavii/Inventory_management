from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from users.models import User
from .models import *
from .forms import *
from .models import *

from datetime import date

from datetime import datetime
from django.urls import reverse
from django.http.response import HttpResponseRedirect, JsonResponse
from django.contrib import messages


import pytz
ist = pytz.timezone('Asia/Kolkata')




def numOfDays(date1):

    dt1 = date1.split('T')

    time = dt1[1]
    time1 = time.split(':')

    dt1 = dt1[0]
    
    dt1 = dt1.split('-')
    

    year = int(dt1[0])
    month = int(dt1[1])
    day = int(dt1[2])

    date1 = datetime(year,month, day , int(time1[0]), int(time1[1]), tzinfo=ist)

    print('--------------')
    print(date1)
    return date1


def get_company_goods_ajax(request):

    data = []
    

    if request.method == "POST":
        company_id = request.POST['company_id']
        try:
            instance = company.objects.filter(id = company_id).first()
            dropdown1 = company_goods.objects.filter(company = instance)
            print(dropdown1)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(dropdown1.values('id', 'name')), safe = False) 


def get_goods_company_ajax(request):

    data = []
    print('i am here')

    if request.method == "POST":
        company_id = request.POST['company_id']
        company_goods_id = request.POST['company_goods']
        print(company_id)
        try:
            company_instance = company.objects.get(id= company_id)
            instance = company_goods.objects.filter(id = company_goods_id).first()
            print(instance)
            dropdown1 = goods_company.objects.filter(company_goods = instance, company_name= company_instance)
            print(dropdown1)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(dropdown1.values('id', 'goods_company_name')), safe = False) 


def get_agent_company_ajax(request):

    data = []
    print('i am here2')

    if request.method == "POST":
        company_id = request.POST['company_id']
        print(company_id)
        try:
            company_instance = company.objects.get(id= company_id)
            print(company_instance)
            
            agent_data = agent.objects.filter(company = company_instance)
            print(agent_data)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(agent_data.values('id', 'name')), safe = False) 

def add_company(request):

    if request.method == 'POST':

        forms = company_Form(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('list_company')
        else:
            print(forms.errors)
    
    else:

        forms = company_Form()

        messages.error(request, 'hsdisdhisidsi')

        context = {
            'form': forms
        }
        return render(request, 'store/add_company.html', context)

        

def update_company(request, company_id):

    if request.method == 'POST':

        instance = company.objects.get(id=company_id)

        forms = company_Form(request.POST, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_company')
        else:
            print(forms.errors)
    
    else:

        instance = company.objects.get(id=company_id)
        forms = company_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'store/add_company.html', context)

        

def delete_company(request, company_id):

    company.objects.get(id=company_id).delete()

    return HttpResponseRedirect(reverse('list_company'))


        

def list_company(request):

    data = company.objects.all()

    context = {
        'data': data
    }

    return render(request, 'store/list_company.html', context)



def add_company_goods(request):
    
    if request.method == 'POST':

        forms = company_goods_Form(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('list_company_goods')
        else:
            print(forms.errors)
            return redirect('add_company_goods')
    
    else:

        forms = company_goods_Form()

        context = {
            'form': forms
        }

        return render(request, 'store/add_company_goods.html', context)

def update_company_goods(request, company_goods_id):

    if request.method == 'POST':

        instance = company_goods.objects.get(id=company_goods_id)

        forms = company_goods_Form(request.POST, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_company_goods')
    
    else:

        instance = company_goods.objects.get(id=company_goods_id)

        forms = company_goods_Form(instance = instance)

        context = {
            'form': forms
        }

        return render(request, 'store/add_company_goods.html', context)


def delete_company_goods(request, company_goods_id):
    
    company_goods.objects.get(id=company_goods_id).delete()

    return HttpResponseRedirect(reverse('list_company_goods'))


def list_company_goods(request):
    
    data = company_goods.objects.all().order_by('company__company_name')

    context = {
            'data': data
        }


    return render(request, 'store/list_company_goods.html', context)



def add_goods_company(request):
    
    if request.method == 'POST':

        forms = goods_company_Form(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('list_goods_company')
        else:
            print(forms.errors)
            return redirect('list_goods_company')
    
    else:

        forms = goods_company_Form()
        data = company.objects.all()
        print(data)

        context = {
            'form': forms,
            'data' : data
        }

        return render(request, 'store/add_goods_company.html', context)

def update_goods_company(request, company_goods_id):

    if request.method == 'POST':

        instance = goods_company.objects.get(id=company_goods_id)

        forms = goods_company_Form(request.POST, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_goods_company')
    
    else:

        instance = goods_company.objects.get(id=company_goods_id)

        forms = goods_company_Form(instance = instance)

        context = {
            'form': forms
        }

        return render(request, 'store/add_goods_company.html', context)


def delete_goods_company(request, company_goods_id):
    
    goods_company.objects.get(id=company_goods_id).delete()

    return HttpResponseRedirect(reverse('list_goods_company'))


def list_goods_company(request):
    
    data = goods_company.objects.all().order_by('company_name__company_name')

    context = {
            'data': data
        }


    return render(request, 'store/list_goods_company.html', context)




def add_agent(request):
    
    if request.method == 'POST':

        forms = agent_Form(request.POST)
        print('-----------------------------1---------------------')
        if forms.is_valid():
            forms.save()
            return redirect('list_agent')
        else:
            print('-----------------------------2---------------------')

            print(forms.errors)
            return redirect('list_agent')
    
    else:

        forms = agent_Form()
        print('--------------------------------------------------')

        
        print(forms)
        print('-----------------------------3---------------------')

        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_agent.html', context)


def update_agent(request, agent_id):

    if request.method == 'POST':

        instance = agent.objects.get(id=agent_id)

        forms = agent_Form(request.POST, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_agent')
    
    else:

        instance = agent.objects.get(id=agent_id)

        forms = agent_Form(instance = instance)

        context = {
            'form': forms
        }

        return render(request, 'store/add_agent.html', context)


def delete_agent(request, agent_id):
    
    agent.objects.get(id=agent_id).delete()

    return HttpResponseRedirect(reverse('list_agent'))


def list_agent(request):
    
    data = agent.objects.all()

    context = {
            'data': data
        }


    return render(request, 'store/list_agent.html', context)
