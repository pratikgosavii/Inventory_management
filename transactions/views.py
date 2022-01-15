from genericpath import samefile
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse

from store.views import numOfDays
from transactions.filters import inward_filter, outward_filter, stock_filter
from .forms import *
from django.shortcuts import render, redirect
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

    try:
        con = inward.objects.filter(id = inward_id).first()

        test = stock.objects.get(company = con.company, company_goods = con.company_goods, goods_company = con.goods_company)
        test.total_bag = test.total_bag - con.bags
        test.save()
        con.delete()

    except:
        print('something went wrong')
        return HttpResponseRedirect(reverse('list_inward'))



    if con:
        return HttpResponseRedirect(reverse('list_inward'))

    else:
        print('something went wrong')




def list_inward(request):

    data = inward.objects.all()

    inward_filter_data = inward_filter()

    context = {
        'data': data,
        'filter_inward' : inward_filter_data
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


def report_dashbord(request):

    inward_filter_data = inward_filter()
    outward_filter_data = outward_filter()



    context = {
            'filter_inward': inward_filter_data,
            'filter_outward': outward_filter_data,
        }

    return render(request, 'transactions/report_dashbord.html', context)


def list_outward(request):

    data = outward.objects.all()

    outward_filter_data = outward_filter()

    

    context = {
        'data': data,
        'filter_outward' : outward_filter_data
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

    try:
        con = outward.objects.filter(id = outward_id).first()

        test = stock.objects.get(company = con.company, company_goods = con.company_goods, goods_company = con.goods_company)
        test.total_bag = test.total_bag + con.bags
        test.save()
        con.delete()

    except:
        print('something went wrong')
        return HttpResponseRedirect(reverse('list_inward'))

    if con:
        return HttpResponseRedirect(reverse('list_outward'))

    else:
        print('something went wrong')



def list_stock(request):

    data = stock.objects.all()
    company_data = company.objects.all()

    inward_filter_data = inward_filter()



    context = {
        'data': data,
        'company' : company_data,
        'filter_inward' : inward_filter_data
    }

    return render(request, 'transactions/list_stock.html', context)


def add_return(request):

    
    if request.method == 'POST':

        forms = supply_return_Form(request.POST)
        DC_date = request.POST.get('DC_date')

        date_time = numOfDays(DC_date)
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



def list_return(request):

    data = supply_return.objects.all()

    # inward_filter_data = inward_filter()

    print(data)

    context = {
        'data': data,
        # 'filter_inward' : inward_filter_data
    }
    
    return render(request, 'transactions/list_return.html', context)


def update_return(request, return_id):

    if request.method == 'POST':

        instance = supply_return.objects.get(id = return_id)

        DC_date = request.POST.get('DC_date')

        date_time = numOfDays(DC_date)
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

        context = {
            'form': forms,
            'comapnyID' : comapnyID,
            'comapny_goods_ID' : comapny_goods_ID,
            'goods_company_ID' : goods_company_ID
        }
        return render(request, 'transactions/update_return.html', context)


def delete_return(request, return_id):

    con = supply_return.objects.get(id = return_id).delete()

    if con:
        return HttpResponseRedirect(reverse('list_return'))

    else:
        print('something went wrong')


def report_inward(request):

    data = inward.objects.all()

    filterd_data = inward_filter(request.GET, data)
    filtered_data = filterd_data.qs
    inward_filter_data = inward_filter()


    company_data = company.objects.all()
    goods_data = company_goods.objects.all()
    goods_company_data = goods_company.objects.all()
    print(filtered_data.count())

    data1 = []
    data2 = []
    

    for i in company_data:
        for j in goods_data:
            for z in goods_company_data:

                inward_total = 0

                final_data = filtered_data.filter(company = i, company_goods = j, goods_company = z)
                
                if final_data:

                    for a in final_data:

                        inward_total = inward_total + a.bags
                    
                        s = final_data.first()
                        data1.append(s.company.company_name)
                        data1.append(s.company_goods)
                        data1.append(s.goods_company)
                        data1.append(inward_total)


                    data2.append(data1)
                    data1 = []

    print(data2)

    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')

    name = "Inward_Report " + time + ".csv"
    
    with open(name,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data2)

    link = os.path.join(BASE_DIR) + '\\' + name

    context = {
        'data': data2,
        'filter_inward' : inward_filter_data,
        'link' : link

        
    }
    
    return render(request, 'report/inward_report.html', context)

    

def report_outward(request):
    
    data = outward.objects.all()

    filterd_data = outward_filter(request.GET, data)
    data = filterd_data.qs
    outward_filter_data = outward_filter()

    company_data = company.objects.all()
    goods_data = company_goods.objects.all()
    goods_company_data = goods_company.objects.all()

    data1 = []
    data2 = []
    

    for i in company_data:
        for j in goods_data:
            for z in goods_company_data:

                inward_total = 0

                final_data = data.filter(company = i, company_goods = j, goods_company = z)
                
                if final_data:
                
                    for a in final_data:

                        inward_total = inward_total + a.bags
                    
                    s = final_data.first()
                    data1.append(s.company.company_name)
                    data1.append(s.company_goods)
                    data1.append(s.goods_company)
                    data1.append(inward_total)


                    data2.append(data1)

                    data1 = []

    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')

    name = "Outward_Report " + time + ".csv"
    
    with open(name,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data2)

    link = os.path.join(BASE_DIR) + '\\' + name
                        

    context = {
        'data': data2,
        'filter_outward' : outward_filter_data,
        'link' : link

        
    }
    
    return render(request, 'report/outward_report.html', context)


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

    name = "Stock_Report " + time + ".csv"
    
    with open(name,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data2)

    stock_filter_data = stock_filter()

    link = os.path.join(BASE_DIR) + '\\' + name



    context = {
        'data': data2,
        'filter_stock' : stock_filter_data,
        'link' : link

    }
    
    return render(request, 'report/stock_report.html', context)




def generate_report_main(request):


    data = inward.objects.all()

    data_inward = inward_filter(request.GET, data)
    data_inward_fil = data_inward.qs

    data_outward = outward.objects.all()

    filterd_data = outward_filter(request.GET, data_outward)
    data_outward_fil = filterd_data.qs
    outward_filter_data = outward_filter()


    company_data = company.objects.all()
    goods_data = company_goods.objects.all()
    goods_company_data = goods_company.objects.all()
    agent_data = agent.objects.all()

    data1 = []
    data2 = []

    for i in company_data:
        for j in goods_data:
            for z in goods_company_data:
                for ag in agent_data:

                   
                    #outward total
                    outward_total = 0
                    final_data_outward = data_outward_fil.filter(company = i, company_goods = j, goods_company = z,  agent = ag)
                    print(final_data_outward)
                    
                    if final_data_outward:
                    
                        for a in final_data_outward:

                            outward_total = outward_total + a.bags

                    return_data = supply_return.objects.filter(company = i, company_goods = j, goods_company = z, agent = ag)

                    total_return_data = 0
                    if return_data:

                        for re in return_data:

                            total_return_data = total_return_data + re.bags

                    net_sale = outward_total - total_return_data

                        
                    #appending data

                    if outward_total != 0:

                      
                        s = final_data_outward.first()
                        data2.append(s.agent.name)
                        data2.append(s.agent.district)
                        data2.append(s.agent.taluka)

                        data2.append(s.company.company_name)
                        data2.append(s.company_goods)
                        data2.append(s.goods_company)

                        data2.append(outward_total)
                        data2.append(total_return_data)
                        data2.append(net_sale)

                        data1.append(data2)

                        final_data_outward = None
                        

                    

                    data2 = [] 
                
                
    
    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')

    name = "Stock_Report " + time + ".csv"
    
    with open(name,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data1)

    
    link = os.path.join(BASE_DIR) + '\\' + name

    

    outward_filter_data = outward_filter()


    context = {
        'data': data1,
        'filter_outward' : outward_filter_data,
        'link' : link

    }
    
    return render(request, 'report/main_report.html', context)


def generate_report_daily(request):

    print(date.today())

    data = inward.objects.filter(DC_date__range=[date.today(), date.today()])
    data_outward = outward.objects.filter(DC_date__range=[date.today(), date.today()])
    print(data, data_outward)

    if data == None and data_outward == None:
        print(' in if ')

        data1 = None
    
        context = {
            'data': data1,

        }
        
        return render(request, 'report/daily_report.html', context)

    else:

        company_data = company.objects.all()
        goods_data = company_goods.objects.all()
        goods_company_data = goods_company.objects.all()

        data1 = []
        data2 = []

        for i in company_data:
            for j in goods_data:
                for z in goods_company_data:

                    #inward total
                    inward_total = 0
                    final_data_inward = data.filter(company = i, company_goods = j, goods_company = z)
                    print(final_data_inward)
                    
                    if final_data_inward:

                        for a in final_data_inward:

                            inward_total = inward_total + a.bags
                    

                    #outward total
                    outward_total = 0
                    final_data_outward = data_outward.filter(company = i, company_goods = j, goods_company = z)
                    print(final_data_outward)
                    
                    if final_data_outward:
                    
                        for a in final_data_outward:

                            outward_total = outward_total + a.bags

                    
                    
                    #appending data
                    
                    print('cheking if')
                    print(final_data_inward)
                    if final_data_inward:
                        print('here1')
                        s = final_data_inward.first()
                        print(s)

                        data2.append(s.company)
                        data2.append(s.company_goods)
                        data2.append(s.goods_company)
                        data2.append(inward_total)
                        data2.append(outward_total)

                    elif final_data_inward != None and final_data_outward == None :
                        print('here2')
                        
                        data2.append(final_data_inward.first())
                        data2.append(inward_total)

                    elif final_data_inward == None and final_data_outward != None :

                        print('here3')

                        data2.append(final_data_outward.first())
                        data2.append(outward_total)
                        
                    #stock total
                    stock_data = stock.objects.filter(company = i, company_goods = j, goods_company = z).first()

                    if final_data_outward:


                        if stock_data:

                            stock_data = stock_data.total_bag

                            data2.append(stock_data)

                            data1.append(data2)


                    data2 = [] 
                    
                    
        
        time =  str(datetime.now(ist))
        time = time.split('.')
        time = time[0].replace(':', '-')

        name = "Daily_Report " + time + ".csv"
        
        with open(name,  'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data1)

        outward_filter_data = outward_filter()

        link = os.path.join(BASE_DIR) + '\\' + name



        context = {
            'data': data1,
            'filter_outward' : outward_filter_data,
            'link' : link

        }
        
        return render(request, 'report/daily_report.html', context)




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
                return response
                

        else:
            print('wrong')



def delete_download(request):

    return render(request, 'delete/dashbaord.html')