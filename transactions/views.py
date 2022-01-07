from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from store.views import numOfDays
from .forms import *
from django.shortcuts import render, redirect
from .models import *
from datetime import date
from django.urls import reverse
import csv

from datetime import datetime
import pytz

import pytz
IST = pytz.timezone('Asia/Kolkata')




# Create your views here.

def add_inward(request):
    
    
    if request.method == 'POST':

        forms = inward_Form(request.POST)
        DC_date = request.POST.get('DC_date')

        date_time = numOfDays(DC_date)
        print('-----------------------------------------------date_time')
        print(date_time.date())
        print(date.today())
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

        forms = inward_Form()

        context = {
            'form': forms
        }
        return render(request, 'transactions/add_inward.html', context)


def update_inward(request, inward_id ):
    
    
    if request.method == 'POST':

        instance = inward.objects.get(id = inward_id)

        DC_date = request.POST.get('DC_date')

        date_time = numOfDays(DC_date)
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

        context = {
            'form': forms,
            'comapnyID' : comapnyID,
            'comapny_goods_ID' : comapny_goods_ID,
            'goods_company_ID' : goods_company_ID
        }
        return render(request, 'transactions/update_inward.html', context)


def delete_inward(request, inward_id):

    con = inward.objects.get(id = inward_id).delete()

    if con:
        return HttpResponseRedirect(reverse('list_inward'))

    else:
        print('something went wrong')




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

            a = forms.cleaned_data['company']
            b = forms.cleaned_data['company_goods']
            c = forms.cleaned_data['goods_company']
            e = forms.cleaned_data['bags']

            try:
                test = stock.objects.get(company = a, company_goods = b, goods_company = c)
                
                test.total_bag = test.total_bag - e
                test.save()

                return redirect('list_outward')
            
            except stock.DoesNotExist:

                print('no stock in inventory')
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


def update_outward(request, outward_id):
    
    
    if request.method == 'POST':

        instance = outward.objects.get(id = outward_id)

        DC_date = request.POST.get('DC_date')

        date_time = numOfDays(DC_date)
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

        instance = outward.objects.get(id = outward_id)
        forms = outward_Form(instance = instance)
        comapnyID = forms.instance.company.id
        comapny_goods_ID = forms.instance.company_goods.id
        goods_company_ID = forms.instance.goods_company.id

        context = {
            'form': forms,
            'comapnyID' : comapnyID,
            'comapny_goods_ID' : comapny_goods_ID,
            'goods_company_ID' : goods_company_ID
        }
        return render(request, 'transactions/update_outward.html', context)


def delete_outward(request, outward_id):

    con = outward.objects.get(id = outward_id).delete()

    if con:
        return HttpResponseRedirect(reverse('list_outward'))

    else:
        print('something went wrong')



def list_stock(request):

    data = stock.objects.all()


    context = {
        'data': data
    }

    return render(request, 'transactions/list_stock.html', context)



def generate_report(request):

    company_data = company.objects.all()
    goods_data = company_goods.objects.all()
    goods_company_data = goods_company.objects.all()

    data1 = []
    data2 = []

    for i in company_data:
        for j in goods_data:
            for z in goods_company_data:

                sample = inward.objects.filter(company = i, company_goods = j, goods_company = z, DC_date__date = datetime.now(IST))
                inward_total = 0
                outward_total = 0
                print('sample')
                print(sample)
                for a in sample:

                    inward_total = inward_total + a.bags
                    print('--------------------------')
                    print(a.DC_date)

                sample = outward.objects.filter(company = i, company_goods = j, goods_company = z, DC_date__date = datetime.now(IST)) 
                print('sample')
                print(sample)

                for a in sample:

                    outward_total = outward_total + a.bags

                stock_data = stock.objects.filter(company = i, company_goods = j, goods_company = z).first()
                
                data2.append(i)

                data2.append(inward_total)
                data2.append(outward_total)
                if stock_data:

                    data2.append(stock_data.total_bag)
                else:
                    data2.append('0')


                data1.append(data2)

                data2 = [] 

    print(date.today())
    
    with open("output.csv",  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data1)


    context = {
        'data2': data1
    }

    return render(request, 'transactions/report.html', context)

