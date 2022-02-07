from email import message
from genericpath import samefile
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

from store.views import numOfDays
from transactions.filters import inward_filter, outward_filter, stock_filter, supply_return_filter
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import date
from django.urls import reverse
import csv
import mimetypes

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


from datetime import datetime
import pytz

IST = pytz.timezone('Asia/Kolkata')




# Create your views here.

@login_required(login_url='login')
def add_inward(request):


    if request.method == 'POST':

        forms = inward_Form(request.POST)
        DC_date = request.POST.get('DC_date')


        if DC_date:

            date_time = numOfDays(DC_date)
        else:
            date_time = datetime.now(IST)
        print('-----------------------------------------------date_time')
        print(date_time)
        updated_request = request.POST.copy()
        updated_request.update({'DC_date': date_time})
        forms = inward_Form(updated_request)

        print(DC_date)

        if forms.is_valid():
            forms.save()

            a = forms.cleaned_data['company']
            b = forms.cleaned_data['company_goods']
            c = forms.cleaned_data['goods_company']
            d = forms.cleaned_data['agent']
            e = forms.cleaned_data['bags']

            try:
                test = stock.objects.get(company = a, company_goods = b, goods_company = c)

                test.total_bag = test.total_bag + e
                test.save()

                return redirect('list_inward')

            except stock.DoesNotExist:

                test = stock.objects.create(company = a, company_goods = b, goods_company = c, total_bag = e)
                return redirect('list_inward')
        else:
            print(forms.errors)

            form = inward_Form()
            context = {
                'form_error': forms.errors
            }
            return render(request, 'transactions/add_inward.html', context)

    else:

        forms = inward_Form()

        context = {
            'form': forms
        }
        return render(request, 'transactions/add_inward.html', context)


@login_required(login_url='login')
def update_inward(request, inward_id ):


    if request.method == 'POST':

        instance = inward.objects.get(id = inward_id)

        company = request.POST.get('company')
        company_goods = request.POST.get('company_goods')
        goods_company = request.POST.get('goods_company')
        bags = request.POST.get('bags')

        if instance.company.company_name != company or instance.company_goods.name != company_goods or instance.goods_company.goods_company_name != goods_company:

            print('in if')

            test = stock.objects.get(company = company, company_goods = company_goods, goods_company = goods_company)
            test.total_bag = test.total_bag + int(bags)
            test.save()
            stock_before = stock.objects.get(company = instance.company.id, company_goods = instance.company_goods.id, goods_company = instance.goods_company.id)
            stock_before.total_bag = stock_before.total_bag - instance.bags
            stock_before.save()

            return HttpResponseRedirect(reverse('list_inward'))


        else:

            DC_date = request.POST.get('DC_date')


            date_time = numOfDays(DC_date)

            if DC_date:

                date_time = numOfDays(DC_date)
            else:
                date_time = datetime.now(IST)

            updated_request = request.POST.copy()
            updated_request.update({'DC_date': date_time})

            forms = inward_Form(updated_request, instance = instance)

            bags_before = forms.instance.bags

            print(DC_date)

            if forms.is_valid():
                forms.save()

                a = forms.cleaned_data['company']
                b = forms.cleaned_data['company_goods']
                c = forms.cleaned_data['goods_company']
                d = forms.cleaned_data['agent']
                bags_after = forms.cleaned_data['bags']

                update_total_minus = None

                print(bags_before)
                print(bags_after)

                if bags_before > bags_after:

                    update_total_minus = bags_before - bags_after
                    print('update_total_minus')
                    print(update_total_minus)

                elif bags_after > bags_before:

                    update_total_plus = bags_after - bags_before
                    print('update_total_plus')
                    print(update_total_plus)

                else:

                    return redirect('list_inward')


                try:
                    test = stock.objects.get(company = a, company_goods = b, goods_company = c)
                    print(test)

                    if update_total_minus != None:

                        test.total_bag = test.total_bag - update_total_minus
                    else:

                        test.total_bag = test.total_bag + update_total_plus

                    test.save()


                    return redirect('list_inward')

                except stock.DoesNotExist:

                    print('no stock in inventory')
                    return redirect('list_intward')

            else:
                print(forms.errors)

    else:

        instance = inward.objects.get(id = inward_id)
        forms = inward_Form(instance = instance)
        comapnyID = forms.instance.company.id
        comapny_goods_ID = forms.instance.company_goods.id
        goods_company_ID = forms.instance.goods_company.id
        agent_ID = forms.instance.agent.id

        context = {
            'form': forms,
            'comapnyID' : comapnyID,
            'comapny_goods_ID' : comapny_goods_ID,
            'goods_company_ID' : goods_company_ID,
            'agent_ID' : agent_ID
        }
        return render(request, 'transactions/update_inward.html', context)


@login_required(login_url='login')
def delete_inward(request, inward_id):

    try:
        con = inward.objects.filter(id = inward_id).first()

        test = stock.objects.get(company = con.company, company_goods = con.company_goods, goods_company = con.goods_company)
        test.total_bag = test.total_bag - con.bags
        test.save()
        con.delete()

        return HttpResponseRedirect(reverse('list_inward_delete'))


    except:
        print('something went wrong')
        return HttpResponseRedirect(reverse('list_inward_delete'))



    if con:
        return HttpResponseRedirect(reverse('list_inward_delete'))

    else:
        print('something went wrong')




@login_required(login_url='login')
def list_inward(request):

    data = inward.objects.all()

    inward_filter_data = inward_filter()

    company_data = company.objects.all()

    context = {
        'data': data,
        'company_data' : company_data,
        'filter_inward' : inward_filter_data
    }

    return render(request, 'transactions/list_inward.html', context)


@login_required(login_url='login')
def add_outward(request):

    if request.method == 'POST':

        forms = outward_Form(request.POST)
        DC_date = request.POST.get('DC_date')

        date_time = numOfDays(DC_date)

        if DC_date:

            date_time = numOfDays(DC_date)
        else:
            date_time = datetime.now(IST)


        updated_request = request.POST.copy()
        updated_request.update({'DC_date': date_time})
        forms = outward_Form(updated_request)

        print(DC_date)



        if forms.is_valid():


            a = forms.cleaned_data['company']
            b = forms.cleaned_data['company_goods']
            c = forms.cleaned_data['goods_company']
            e = forms.cleaned_data['bags']

            try:
                test = stock.objects.get(company = a, company_goods = b, goods_company = c)

                if test.total_bag >= e:

                    test.total_bag = test.total_bag - e
                    test.save()
                    forms.save()

                    return redirect('list_outward')

                else:
                    messages.error(request, "Outward is more than Stock")
                    print('Outward is more than Stock')
                    return redirect('list_outward')


            except stock.DoesNotExist:

                messages.error(request, 'no stock in inventory for outward')
                return redirect('list_outward')


        else:
            print(forms.errors)

    else:

        forms = outward_Form()

        context = {
            'form': forms
        }
        return render(request, 'transactions/add_outward.html', context)


@login_required(login_url='login')
def report_dashbord(request):

    inward_filter_data = inward_filter()
    outward_filter_data = outward_filter()



    context = {
            'filter_inward': inward_filter_data,
            'filter_outward': outward_filter_data,
        }

    return render(request, 'transactions/report_dashbord.html', context)


@login_required(login_url='login')
def list_outward(request):

    data = outward.objects.all()

    outward_filter_data = outward_filter()

    company_data = company.objects.all()

    context = {
        'data': data,
        'filter_outward' : outward_filter_data,
        'company_data' : company_data
    }

    return render(request, 'transactions/list_outward.html', context)

@login_required(login_url='login')
def update_outward(request, outward_id):


    if request.method == 'POST':

        instance = outward.objects.get(id = outward_id)

        company = request.POST.get('company')
        company_goods = request.POST.get('company_goods')
        goods_company = request.POST.get('goods_company')
        bags = request.POST.get('bags')

        if instance.company.company_name != company or instance.company_goods.name != company_goods or instance.goods_company.goods_company_name != goods_company:

            print('in if')

            test = stock.objects.get(company = company, company_goods = company_goods, goods_company = goods_company)
            test.total_bag = test.total_bag - int(bags)
            test.save()
            stock_before = stock.objects.get(company = instance.company.id, company_goods = instance.company_goods.id, goods_company = instance.goods_company.id)
            stock_before.total_bag = stock_before.total_bag + instance.bags
            stock_before.save()

            return HttpResponseRedirect(reverse('list_outward'))


        else:
            DC_date = request.POST.get('DC_date')

            date_time = numOfDays(DC_date)

            if DC_date:

                date_time = numOfDays(DC_date)
            else:
                date_time = datetime.now(IST)


            updated_request = request.POST.copy()
            updated_request.update({'DC_date': date_time})

            forms = outward_Form(updated_request, instance = instance)

            print(DC_date)

            bags_before = forms.instance.bags


            if forms.is_valid():
                forms.save()

                a = forms.cleaned_data['company']
                b = forms.cleaned_data['company_goods']
                c = forms.cleaned_data['goods_company']
                d = forms.cleaned_data['agent']
                bags_after = forms.cleaned_data['bags']

                update_total_minus = None

                print(bags_before)
                print(bags_after)

                if bags_before < bags_after:

                    update_total_minus = bags_after - bags_before
                    print('update_total_minus')
                    print(update_total_minus)

                elif bags_before > bags_after:

                    update_total_plus = bags_before - bags_after
                    print('update_total_plus')
                    print(update_total_plus)

                else:

                    return redirect('list_inward')


                try:
                    test = stock.objects.get(company = a, company_goods = b, goods_company = c)
                    print(test)

                    if update_total_minus:

                        test.total_bag = test.total_bag - update_total_minus
                    else:

                        test.total_bag = test.total_bag + update_total_plus

                    test.save()


                    return redirect('list_inward')

                except stock.DoesNotExist:

                    print('no stock in inventory')
                    return redirect('list_intward')

            else:
                print(forms.errors)

    else:

        instance = outward.objects.get(id = outward_id)
        forms = outward_Form(instance = instance)
        comapnyID = forms.instance.company.id
        comapny_goods_ID = forms.instance.company_goods.id
        goods_company_ID = forms.instance.goods_company.id
        agent_ID = forms.instance.agent.id

        context = {
            'form': forms,
            'comapnyID' : comapnyID,
            'comapny_goods_ID' : comapny_goods_ID,
            'goods_company_ID' : goods_company_ID,
            'agent_ID' : agent_ID
        }
        return render(request, 'transactions/update_outward.html', context)


@login_required(login_url='login')
def delete_outward(request, outward_id):

    try:
        con = outward.objects.get(id = outward_id)

        test = stock.objects.get(company = con.company, company_goods = con.company_goods, goods_company = con.goods_company)
        test.total_bag = test.total_bag + con.bags
        test.save()
        con.delete()

        return HttpResponseRedirect(reverse('list_outward_delete'))


    except:
        print('something went wrong')
        return HttpResponseRedirect(reverse('list_outward_delete'))


@login_required(login_url='login')
def list_stock(request):

    data = stock.objects.all()

    stock_filter_data = stock_filter()

    company_data = company.objects.all()

    context = {
        'data': data,
        'stock_filter' : stock_filter_data,
        'company_data': company_data
    }

    return render(request, 'transactions/list_stock.html', context)


@login_required(login_url='login')
def add_return(request):


    if request.method == 'POST':

        forms = supply_return_Form(request.POST)
        DC_date = request.POST.get('DC_date')

        date_time = numOfDays(DC_date)

        if DC_date:

            date_time = numOfDays(DC_date)
        else:
            date_time = datetime.now(IST)


        print('-----------------------------------------------date_time')
        print(date_time.date())
        print(date.today())
        updated_request = request.POST.copy()
        updated_request.update({'DC_date': date_time})
        forms = supply_return_Form(updated_request)

        print(DC_date)

        if forms.is_valid():
            forms.save()

            a = forms.cleaned_data['company']
            b = forms.cleaned_data['company_goods']
            c = forms.cleaned_data['goods_company']
            d = forms.cleaned_data['agent']
            e = forms.cleaned_data['bags']

            try:

                test = stock.objects.get(company = a, company_goods = b, goods_company = c)

                test.total_bag = test.total_bag + e
                test.save()

                return redirect('list_return')

            except stock.DoesNotExist:

                test = stock.objects.create(company = a, company_goods = b, goods_company = c, total_bag = e)
                return redirect('list_inward')

        else:
            print(forms.error)

    else:

        forms = supply_return_Form()

        context = {
            'form': forms
        }
        return render(request, 'transactions/add_return.html', context)



@login_required(login_url='login')
def list_return(request):

    data = supply_return.objects.all()

    supply_return_filter_data = supply_return_filter()

    # inward_filter_data = inward_filter()

    print(data)

    company_data = company.objects.all()

    context = {
        'data': data,
        'company_data': company_data,
        'filter_return_supply' : supply_return_filter_data
    }

    return render(request, 'transactions/list_return.html', context)


@login_required(login_url='login')
def update_return(request, return_id):

    if request.method == 'POST':

        instance = supply_return.objects.get(id = return_id)

        company = request.POST.get('company')
        company_goods = request.POST.get('company_goods')
        goods_company = request.POST.get('goods_company')
        bags = request.POST.get('bags')

        if instance.company.company_name != company or instance.company_goods.name != company_goods or instance.goods_company.goods_company_name != goods_company:

            test = stock.objects.get(company = company, company_goods = company_goods, goods_company = goods_company)
            test.total_bag = test.total_bag + int(bags)
            test.save()
            stock_before = stock.objects.get(company = instance.company.id, company_goods = instance.company_goods.id, goods_company = instance.goods_company.id)
            stock_before.total_bag = stock_before.total_bag - instance.bags
            stock_before.save()


            return HttpResponseRedirect(reverse('list_return'))


        else:

            DC_date = request.POST.get('DC_date')

            date_time = numOfDays(DC_date)

            if DC_date:

                date_time = numOfDays(DC_date)
            else:
                date_time = datetime.now(IST)


            updated_request = request.POST.copy()
            updated_request.update({'DC_date': date_time})

            forms = supply_return_Form(updated_request, instance = instance)

            bags_before = forms.instance.bags

            print(DC_date)

            if forms.is_valid():
                forms.save()

                a = forms.cleaned_data['company']
                b = forms.cleaned_data['company_goods']
                c = forms.cleaned_data['goods_company']
                d = forms.cleaned_data['agent']
                bags_after = forms.cleaned_data['bags']

                update_total_minus = None
                update_total_plus = None

                print(bags_before)
                print(bags_after)


                if bags_before < bags_after:

                    update_total_plus = bags_after - bags_before


                elif bags_before > bags_after:

                    update_total_minus = bags_before - bags_after


                else:

                    return redirect('list_inward')


                try:
                    test = stock.objects.get(company = a, company_goods = b, goods_company = c)
                    print(test)

                    if update_total_minus != None:

                        test.total_bag = test.total_bag - update_total_minus
                    else:

                        test.total_bag = test.total_bag + update_total_plus

                    test.save()


                    return redirect('list_return')

                except stock.DoesNotExist:

                    print('no stock in inventory')
                    return redirect('list_return')

            else:
                print(forms.errors)

    else:

        instance = supply_return.objects.get(id = return_id)
        forms = supply_return_Form(instance = instance)
        comapnyID = forms.instance.company.id
        comapny_goods_ID = forms.instance.company_goods.id
        goods_company_ID = forms.instance.goods_company.id
        agent_ID = forms.instance.agent.id

        context = {
            'form': forms,
            'comapnyID' : comapnyID,
            'comapny_goods_ID' : comapny_goods_ID,
            'goods_company_ID' : goods_company_ID,
            'agent_ID' : agent_ID       
        }
        return render(request, 'transactions/update_return.html', context)


@login_required(login_url='login')
def delete_return(request, return_id):

    try:
        con = supply_return.objects.get(id = return_id)
        print(con)
        test = stock.objects.get(company = con.company, company_goods = con.company_goods, goods_company = con.goods_company)
        test.total_bag = test.total_bag - con.bags
        test.save()
        con.delete()

        return HttpResponseRedirect(reverse('list_return'))


    except:
        print('something went wrong')
        return HttpResponseRedirect(reverse('list_return'))
 
        


@login_required(login_url='login')
def report_inward(request):

    data = inward.objects.all()

    filterd_data = inward_filter(request.GET, data)
    filtered_data = filterd_data.qs
    inward_filter_data = inward_filter()


    company_data = company.objects.all()
    company_goods_data = company_goods.objects.all()
    goods_company_data = goods_company.objects.all()

    company_data = pd.DataFrame(list(company.objects.all().values('id', 'company_name')))
    company_data = dict(company_data.values)

    company_goods_data = pd.DataFrame(list(company_goods.objects.all().values('id', 'name')))
    company_goods_data = dict(company_goods_data.values)

    goods_company_data = pd.DataFrame(list(goods_company.objects.all().values('id', 'goods_company_name')))
    goods_company_data = dict(goods_company_data.values)

   
    # agent_data = pd.DataFrame(list(agent.objects.all().values('id', 'name')))
    # agent_data = dict(agent_data.values)

    df = pd.DataFrame(list(filtered_data.values()))

    sum__ = df.groupby(['company_id', 'company_goods_id', 'goods_company_id']).sum().reset_index()


    sum__['company_id'] = sum__['company_id'].map(company_data)
    sum__['company_goods_id'] = sum__['company_goods_id'].map(company_goods_data)
    sum__['goods_company_id'] = sum__['goods_company_id'].map(goods_company_data)
    # sum__['agent_id'] = sum__['agent_id'].map(agent_data)

    del sum__['agent_id']
    del sum__['id']

    print(sum__)

    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')
    vals = sum__.values

    name = "Daily_Report " + time + ".csv"
    path = os.path.join(BASE_DIR) + '\static\csv\\' + name
    with open(path,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(vals)


    link = os.path.join(BASE_DIR) + '\static\csv\\' + name

    vals_list = (vals.tolist())

    print(vals_list)

    context = {
        'data': vals_list,
        'filter_inward' : inward_filter_data,
        'link' : link


    }

    return render(request, 'report/inward_report.html', context)



@login_required(login_url='login')
def report_outward(request):

    data = outward.objects.all()

    filterd_data = outward_filter(request.GET, data)
    outward_filter_data = outward_filter()

    company_data = company.objects.all()
    company_goods_data = company_goods.objects.all()
    goods_company_data = goods_company.objects.all()
 

    company_data = pd.DataFrame(list(company.objects.all().values('id', 'company_name')))
    company_data = dict(company_data.values)

    company_goods_data = pd.DataFrame(list(company_goods.objects.all().values('id', 'name')))
    company_goods_data = dict(company_goods_data.values)

    goods_company_data = pd.DataFrame(list(goods_company.objects.all().values('id', 'goods_company_name')))
    goods_company_data = dict(goods_company_data.values)

    
    agent_data = pd.DataFrame(list(agent.objects.all().values('id', 'name')))
    agent_data = dict(agent_data.values)

    agent_data2 = pd.DataFrame(list(agent.objects.all().values('id', 'name', 'place', 'taluka', 'district')))

    df = pd.DataFrame(list(filterd_data.qs.values()))

    sum__ = df.groupby(['company_id', 'company_goods_id', 'goods_company_id', 'agent_id']).sum().reset_index()

    print('all right')

    sum__['company_id'] = sum__['company_id'].map(company_data)
    sum__['company_goods_id'] = sum__['company_goods_id'].map(company_goods_data)
    sum__['goods_company_id'] = sum__['goods_company_id'].map(goods_company_data)
    sum__['agent_id'] = sum__['agent_id'].map(agent_data)

    out = (sum__.merge(agent_data2, left_on='agent_id', right_on='name').reindex(columns=['agent_id', 'place', 'taluka', 'district', 'company_id', 'company_goods_id', 'goods_company_id', 'bags']))

    sum__ = out

    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')
    vals = sum__.values

    print(vals)


    name = "Daily_Report " + time + ".csv"
    path = os.path.join(BASE_DIR) + '\static\csv\\' + name
    with open(path,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(vals)

    link = os.path.join(BASE_DIR) + '\static\csv\\' + name

    vals_list = (vals.tolist())


    context = {
        'data': vals_list,
        'filter_outward' : outward_filter_data,
        'link' : link


    }

    return render(request, 'report/outward_report.html', context)




@login_required(login_url='login')
def report_supply_return(request):

    data = supply_return.objects.all()

    filterd_data = supply_return_filter(request.GET, data)
    data = filterd_data.qs

    company_data = pd.DataFrame(list(company.objects.all().values('id', 'company_name')))
    company_data = dict(company_data.values)

    company_goods_data = pd.DataFrame(list(company_goods.objects.all().values('id', 'name')))
    company_goods_data = dict(company_goods_data.values)

    goods_company_data = pd.DataFrame(list(goods_company.objects.all().values('id', 'goods_company_name')))
    goods_company_data = dict(goods_company_data.values)

    
    agent_data = pd.DataFrame(list(agent.objects.all().values('id', 'name')))
    agent_data = dict(agent_data.values)

    agent_data2 = pd.DataFrame(list(agent.objects.all().values('id', 'name', 'place', 'taluka', 'district')))

    df = pd.DataFrame(list(filterd_data.qs.values()))

    sum__ = df.groupby(['company_id', 'company_goods_id', 'goods_company_id', 'agent_id']).sum().reset_index()

    print('all right')

    sum__['company_id'] = sum__['company_id'].map(company_data)
    sum__['company_goods_id'] = sum__['company_goods_id'].map(company_goods_data)
    sum__['goods_company_id'] = sum__['goods_company_id'].map(goods_company_data)
    sum__['agent_id'] = sum__['agent_id'].map(agent_data)

    out = (sum__.merge(agent_data2, left_on='agent_id', right_on='name').reindex(columns=['agent_id', 'place', 'taluka', 'district', 'company_id', 'company_goods_id', 'goods_company_id', 'bags']))

    sum__ = out

    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')
    vals = sum__.values

    print(vals)


    name = "Daily_Report " + time + ".csv"
    path = os.path.join(BASE_DIR) + '\static\csv\\' + name
    with open(path,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(vals)

    link = os.path.join(BASE_DIR) + '\static\csv\\' + name

    vals_list = (vals.tolist())


    context = {
        'data': vals_list,
        'link' : link,

    }

    return render(request, 'report/outward_report.html', context)


@login_required(login_url='login')
def generate_report_stock(request):

    print('i am here')

    data = stock.objects.all()

    data_stock = stock_filter(request.GET, data)
    data_stock = data_stock.qs

    data1 = []
    data2 = []





    if data_stock:

        for i in data_stock:

            print('(i.company.company_name')
            print(i.company.company_name)

            data1.append(i.company.company_name)
            data1.append(i.company_goods)
            data1.append(i.goods_company)
            data1.append(i.total_bag)




            data2.append(data1)

            data1 = []



    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')

    name = "Daily_Report " + time + ".csv"
    path = os.path.join(BASE_DIR) + '\static\csv\\' + name
    with open(path,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data2)

    link = os.path.join(BASE_DIR) + '\static\csv\\' + name

    stock_filter_data = stock_filter()

    context = {
        'data': data2,
        'stock_filter' : stock_filter_data,
        'link' : link

    }

    return render(request, 'report/stock_report.html', context)




@login_required(login_url='login')
def generate_report_main(request):

    company_data = pd.DataFrame(list(company.objects.all().values('id', 'company_name')))
    company_data = dict(company_data.values)

    company_goods_data = pd.DataFrame(list(company_goods.objects.all().values('id', 'name')))
    company_goods_data = dict(company_goods_data.values)

    goods_company_data = pd.DataFrame(list(goods_company.objects.all().values('id', 'goods_company_name')))
    goods_company_data = dict(goods_company_data.values)

    agent_data = pd.DataFrame(list(agent.objects.all().values('id', 'name')))
    agent_data = dict(agent_data.values)
    
    agent_data2 = pd.DataFrame(list(agent.objects.all().values('id', 'name', 'place', 'taluka', 'district')))

    print(agent_data2)


    # return_data = supply_return.objects.all()

    outward_data = outward.objects.all()
    supply_return_data = supply_return.objects.all()
    outward_filterd_data = outward_filter(request.GET, outward_data)
    supply_return_filterd_data = outward_filter(request.GET, supply_return_data)

    df = pd.DataFrame(list(outward_filterd_data.qs.values()))

    sum__ = df.groupby(['company_id', 'company_goods_id', 'goods_company_id', 'agent_id']).sum().reset_index()

    print(sum__)
    df2 = pd.DataFrame(list(supply_return_filterd_data.qs.values()))

    sum__2 = df2.groupby(['company_id', 'company_goods_id', 'goods_company_id', 'agent_id']).sum().reset_index()

    print(sum__2)
    final_ou = pd.merge(sum__, sum__2, on=['company_id', 'company_goods_id', 'goods_company_id', 'agent_id'], how="outer")[['company_id', 'company_goods_id', 'goods_company_id', 'agent_id', 'bags_x', 'bags_y']]

    final_ou['bagsz'] = final_ou['bags_x'] - final_ou['bags_y']

    print(final_ou)

    final_ou['company_id'] = final_ou['company_id'].map(company_data)
    final_ou['company_goods_id'] = final_ou['company_goods_id'].map(company_goods_data)
    final_ou['goods_company_id'] = final_ou['goods_company_id'].map(goods_company_data)
    final_ou['agent_id'] = final_ou['agent_id'].map(agent_data)

    # print(final_ou)
    # here
    out = (final_ou.merge(agent_data2, left_on='agent_id', right_on='name').reindex(columns=['agent_id', 'place', 'taluka', 'district','company_id', 'company_goods_id', 'goods_company_id', 'bags_x', 'bags_y', 'bagsz']))

    # print(out)
    vals = out.values

    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')

    name = "Daily_Report " + time + ".csv"
    path = os.path.join(BASE_DIR) + '\static\csv\\' + name
    with open(path,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(vals)


    link = os.path.join(BASE_DIR) + '\static\csv\\' + name


    outward_filter_data = outward_filter()

    vals_list = (vals.tolist())

    company_data = company.objects.all()

    context = {
        'data' : vals_list,
        'filter_outward' : outward_filter_data,
        'link' : link,
        'company_data' : company_data

    }

    return render(request, 'report/main_report.html', context)
    

@login_required(login_url='login')
def generate_report_daily(request):

    print(date.today())

    data = inward.objects.filter(DC_date__date=date.today())
    data_outward = outward.objects.filter(DC_date__date=date.today())
    print('data first')
    print(data, data_outward)

    if data == None or data_outward == None:
        print(' in if ')

        data1 = None

        context = {
            'data': data1,

        }

        return render(request, 'report/daily_report.html', context)

    else:

        company_data = company.objects.all()
        company_goods_data = company_goods.objects.all()
        goods_company_data = goods_company.objects.all()
        agent_data = agent.objects.all()

        company_data = pd.DataFrame(list(company.objects.all().values('id', 'company_name')))
        company_data = dict(company_data.values)

        company_goods_data = pd.DataFrame(list(company_goods.objects.all().values('id', 'name')))
        company_goods_data = dict(company_goods_data.values)

        goods_company_data = pd.DataFrame(list(goods_company.objects.all().values('id', 'goods_company_name')))
        goods_company_data = dict(goods_company_data.values)

        agent_data = pd.DataFrame(list(agent.objects.all().values('id', 'name')))
        agent_data = dict(agent_data.values)

        # inward sum
        df = pd.DataFrame(list(inward.objects.all().values()))

        sum__ = df.groupby(['company_id', 'company_goods_id', 'goods_company_id', 'agent_id']).sum().reset_index()

        # outward sum
        df2 = pd.DataFrame(list(outward.objects.all().values()))

        sum__2 = df2.groupby(['company_id', 'company_goods_id', 'goods_company_id', 'agent_id']).sum().reset_index()

        # adding inward and return 
        final_ou = pd.merge(sum__, sum__2, on=['company_id', 'company_goods_id', 'goods_company_id', 'agent_id'])[['company_id', 'company_goods_id', 'goods_company_id', 'agent_id', 'bags_x', 'bags_y']]

        final_ou['bagsz'] = final_ou['bags_x'] +  final_ou['bags_y']

        #return sum
        df3 = pd.DataFrame(list(supply_return.objects.all().values()))

        sum__3 = df3.groupby(['company_id', 'company_goods_id', 'goods_company_id', 'agent_id']).sum().reset_index()

        print(sum__3)

        final_out = pd.merge(final_ou, sum__3, on=['company_id', 'company_goods_id', 'goods_company_id', 'agent_id'])[['company_id', 'company_goods_id', 'goods_company_id', 'agent_id', 'bagsz', 'bags']]
        final_out['bags_final'] = final_out['bagsz'] - final_out['bags']

        final_out['company_id'] = final_out['company_id'].map(company_data)
        final_out['company_goods_id'] = final_out['company_goods_id'].map(company_goods_data)
        final_out['goods_company_id'] = final_out['goods_company_id'].map(goods_company_data)
        final_out['agent_id'] = final_out['agent_id'].map(agent_data)

        print(final_out)

        vals = final_out.values
       
        time =  str(datetime.now(ist))
        time = time.split('.')
        time = time[0].replace(':', '-')

        name = "Daily_Report " + time + ".csv"
        path = os.path.join(BASE_DIR) + '\static\csv\\' + name
        with open(path,  'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerows(vals)

        outward_filter_data = outward_filter()

        link = os.path.join(BASE_DIR) + '\static\csv\\' + name

        vals_list = (vals.tolist())


        context = {
            'data': vals_list,
            'filter_outward' : outward_filter_data,
            'link' : link

        }

        return render(request, 'report/daily_report.html', context)




@login_required(login_url='login')
def download(request):
    # fill these variables with real values


    if request.method == 'POST':

        fl_path =  request.POST.get('link')



        if os.path.exists(fl_path):

            with open(fl_path, 'r' ) as fh:
                mime_type  = mimetypes.guess_type(fl_path)
                print('--------------------')
                print(mime_type)
                response = HttpResponse(fh.read(), content_type=mime_type)
                response['Content-Disposition'] = 'attachment;filename=' + str(fl_path)
                # a =  _delete_file(fl_path)

                return response



        else:
            messages.error(request, 'path does not exist')


def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

       return 'abc'

@login_required(login_url='login')
def delete_dashboard(request):

    return render(request, 'delete/dashbaord.html')


# delete view


def list_inward_delete(request):

    data = inward.objects.all()

    inward_filter_data = inward_filter()

    context = {
        'data': data,
        'filter_inward' : inward_filter_data
    }

    return render(request, 'delete/list_inward_delete.html', context)


def list_outward_delete(request):

    data = outward.objects.all()

    outward_filter_data = outward_filter()



    context = {
        'data': data,
        'filter_outward' : outward_filter_data
    }

    return render(request, 'delete/list_outward_delete.html', context)

def list_return_delete(request):

    data = supply_return.objects.all()

    # inward_filter_data = inward_filter()

    print(data)

    context = {
        'data': data,
        # 'filter_inward' : inward_filter_data
    }

    return render(request, 'delete/list_return_delete.html', context)

