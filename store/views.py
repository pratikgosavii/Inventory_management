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

   
    return date1


@login_required(login_url='login')
def get_company_goods_ajax(request):

    data = []
    

    if request.method == "POST":
        company_id = request.POST['company_id']
        try:
            instance = company.objects.filter(id = company_id).first()
            dropdown1 = company_goods.objects.filter(company = instance)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(dropdown1.values('id', 'name')), safe = False) 


@login_required(login_url='login')
def get_goods_company_ajax(request):

    data = []

    if request.method == "POST":
        company_id = request.POST['company_id']
        company_goods_id = request.POST['company_goods']
        try:
            company_instance = company.objects.get(id= company_id)
            instance = company_goods.objects.filter(id = company_goods_id).first()
            dropdown1 = goods_company.objects.filter(company_goods = instance, company_name= company_instance)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(dropdown1.values('id', 'goods_company_name')), safe = False) 


@login_required(login_url='login')
def get_agent_company_ajax(request):

    data = []

    if request.method == "POST":
        company_id = request.POST['company_id']
        try:
            company_instance = company.objects.get(id= company_id)
            
            agent_data = agent.objects.filter(company = company_instance)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(agent_data.values('id', 'name')), safe = False) 

@login_required(login_url='login')
def add_company(request):

    if request.method == 'POST':

        forms = company_Form(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('list_company')
        else:

            
            context = {
                'form': forms
            }

            return render(request, 'store/add_company.html', context)

    else:

        forms = company_Form()

        context = {
            'form': forms
        }
        return render(request, 'store/add_company.html', context)

        

@login_required(login_url='login')
def update_company(request, company_id):

    if request.method == 'POST':

        instance = company.objects.get(id=company_id)

        forms = company_Form(request.POST, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_company')
        else:
            context = {
                'form': forms
            }
            return render(request, 'store/add_company.html', context)


    else:

        instance = company.objects.get(id=company_id)
        forms = company_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'store/add_company.html', context)

        

@login_required(login_url='login')
def delete_company(request, company_id):

    company.objects.get(id=company_id).delete()

    return HttpResponseRedirect(reverse('list_company_delete'))


        

@login_required(login_url='login')
def list_company(request):

    data = company.objects.all()

    context = {
        'data': data
    }

    return render(request, 'store/list_company.html', context)



@login_required(login_url='login')
def add_company_goods(request):
    
    if request.method == 'POST':

        forms = company_goods_Form(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('list_company_goods')
        else:
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
            pass
    
    else:

        instance = company_goods.objects.get(id=company_goods_id)

        forms = company_goods_Form(instance = instance)

        comapnyID = instance.company.id
        comapny_goods_ID = instance.id

      
        context = {
            'form': forms,
            'comapnyID' : comapnyID,
            'comapny_goods_ID' : comapny_goods_ID
            
        }

        return render(request, 'store/update_company_goods.html', context)


@login_required(login_url='login')
def delete_company_goods(request, company_goods_id):
    
    company_goods.objects.get(id=company_goods_id).delete()

    return HttpResponseRedirect(reverse('list_company_goods_delete'))


@login_required(login_url='login')
def list_company_goods(request):
    
    data = company_goods.objects.all().order_by('company__company_name')

    context = {
            'data': data
        }


    return render(request, 'store/list_company_goods.html', context)



@login_required(login_url='login')
def add_goods_company(request):
    
    if request.method == 'POST':

        forms = goods_company_Form(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('list_goods_company')
        else:
            return redirect('list_goods_company')
    
    else:

        forms = goods_company_Form()
        data = company.objects.all()

        context = {
            'form': forms,
            'data' : data,
        }

        return render(request, 'store/add_goods_company.html', context)

@login_required(login_url='login')
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
        comapny_goods_ID = instance.company_goods.id

   
        context = {
            'form': forms,
            'comapnyID' : instance.company_name.id,
            'comapny_goods_ID' : comapny_goods_ID,
        }

        return render(request, 'store/update_goods_company.html', context)


@login_required(login_url='login')
def delete_goods_company(request, company_goods_id):
    
    goods_company.objects.get(id=company_goods_id).delete()

    return HttpResponseRedirect(reverse('list_goods_company_delete'))


@login_required(login_url='login')
def list_goods_company(request):
    
    data = goods_company.objects.all().order_by('company_name__company_name')

    context = {
            'data': data
        }


    return render(request, 'store/list_goods_company.html', context)




@login_required(login_url='login')
def add_agent(request):
    
    if request.method == 'POST':

        forms = agent_Form(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('list_agent')
        else:
          
            return redirect('list_agent')
    
    else:

        forms = agent_Form()
      
        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_agent.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def delete_agent(request, agent_id):
    
    agent.objects.get(id=agent_id).delete()

    return HttpResponseRedirect(reverse('list_agent_delete'))


@login_required(login_url='login')
def list_agent(request):
    
    data = agent.objects.all()

    context = {
            'data': data
        }


    return render(request, 'store/list_agent.html', context)




@login_required(login_url='login')
def add_transport(request):
    
    if request.method == 'POST':

        forms = transport_Form(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('list_transport')
        else:
          
            return redirect('list_transport')
    
    else:

        forms = transport_Form()
       
        company_data = company.objects.all()

        context = {
            'form': forms,
            'company' : company_data
        }

        return render(request, 'store/add_transport.html', context)


@login_required(login_url='login')
def update_transport(request, transport_id):

    if request.method == 'POST':

        instance = transport.objects.get(id=transport_id)

        forms = transport_Form(request.POST, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_transport')
    
    else:

        instance = transport.objects.get(id=transport_id)

        forms = transport_Form(instance = instance)

        context = {
            'form': forms
        }

        return render(request, 'store/add_transport.html', context)


@login_required(login_url='login')
def delete_transport(request, transport_id):
    
    transport.objects.get(id=transport_id).delete()

    return HttpResponseRedirect(reverse('list_transport_delete'))


@login_required(login_url='login')
def list_transport(request):
    
    data = transport.objects.all()

    context = {
            'data': data
        }


    return render(request, 'store/list_transport.html', context)



# delete view

     

@login_required(login_url='login')
def list_company_delete(request):

    data = company.objects.all()

    context = {
        'data': data
    }

    return render(request, 'delete/list_company_delete.html', context)


@login_required(login_url='login')
def list_company_delete(request):

    data = company.objects.all()

    context = {
        'data': data
    }

    return render(request, 'delete/list_company_delete.html', context)



@login_required(login_url='login')
def list_company_goods_delete(request):
    
    data = company_goods.objects.all().order_by('company__company_name')

    context = {
            'data': data
        }


    return render(request, 'delete/list_company_goods_delete.html', context)



@login_required(login_url='login')
def list_goods_company_delete(request):
    
    data = goods_company.objects.all().order_by('company_name__company_name')

    context = {
            'data': data
        }


    return render(request, 'delete/list_goods_company_delete.html', context)




@login_required(login_url='login')
def list_agent_delete(request):
    
    data = agent.objects.all()

    context = {
            'data': data
        }


    return render(request, 'delete/list_agent_delete.html', context)


@login_required(login_url='login')
def list_transport_delete(request):
    
    data = transport.objects.all()

    context = {
            'data': data
        }


    return render(request, 'delete/list_transport_delete.html', context)

