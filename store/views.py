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
from django.http.response import HttpResponseRedirect


import pytz
ist = pytz.timezone('Asia/Kolkata')



def numOfDays(date1):

    dt1 = date1.split('T')

    time = dt1[1]
    time1 = time.split(':')

    dt1 = dt1[0]
    
    for i in dt1:
        print(i)

    year = int(dt1[0])
    month = int(dt1[0])
    day = int(dt1[0])

    date1 = datetime(year, month, day, int(time1[0]), int(time1[1]), tzinfo=ist)

    print(date1)
    return date1


@login_required(login_url='login')
def create_brand(request):
    forms = BrandForm()
    if request.method == 'POST':
        forms = BrandForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('brand-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_product.html', context)


class BrandListView(ListView):
    model = Brand
    template_name = 'store/brand_list.html'
    context_object_name = 'product'

def update_brand(request):
    pass

def delete_brand(request):
    pass


def add_product(request):

    if request.method == "GET":



        forms = ProductForm()
        brand_id = request.GET.get('brand_id')
        print('--------------------------------------------')
        print(brand_id)
        
        context = {
            'form': forms,
            'brand_id':brand_id
        }

        return render(request, 'store/add_products.html', context)

    else:

        forms = ProductForm()
        if request.method == 'POST':
            data = request.POST.get('date_data')
            brand = request.POST.get('brand_id')
            Brand_data = Brand.objects.get(id=brand)
            print(data)
            print(data)
            date_time = numOfDays(data)
            updated_request = request.POST.copy()
            updated_request.update({'date_time': date_time})
            forms = ProductForm(updated_request)
            if forms.is_valid():
                instance = forms.save(commit=False)
                instance.brand = Brand_data
               
                instance.save()
                
                return HttpResponseRedirect(reverse('view-product', kwargs={'brand_id':brand}))

            else:
                print(forms.errors)
            data = Brand_Product.objects.all()

            context = {
                'data': data
            }

            return render(request, 'store/create_delivery.html', context)


def list_product(request, brand_id):

    brand = Brand.objects.get(id=brand_id)
    
    data = Brand_Product.objects.filter(brand=brand)
    print()

    context = {
        'data': data,
        'brand_id' : brand_id
    }
    
    return render(request, 'store/products_list.html', context)

def update_product(request, id=None):

#     if request.method == 'POST':

#         data = request.POST.get('date_data')
#         brand = request.POST.get('brand_id')
#         Brand_data = Brand.objects.get(id=brand)
#         print(data)
#         print(data)
#         date_time = numOfDays(data)
#         updated_request = request.POST.copy()
#         updated_request.update({'date_time': date_time})
#         forms = ProductForm(updated_request)

#         if forms.is_valid():
#             instance = forms.save(commit=False)
#             instance.brand = Brand_data
        
#             instance.save()

            
#             form = ProductForm(instance=instance)

#             context = {
#                 'form': instance,
            
#             }
            
#             return render(request, 'store/update_product.html', context)

#     else:
#         data = Brand_Product.objects.get(id=id)

#         form = ProductForm(instance=data)

#         context = {
#             'form': form,
#             'brand_id':brand_id
        
#         }
        
#         return render(request, 'store/update_product.html', context)
    
    pass

def delete_product(request, id):
    
    data = Brand_Product.objects.get(id=id)
    brand_id = data.brand.id
    data.delete()



    return HttpResponseRedirect(reverse('view-product', kwargs={'brand_id':brand_id}))


    pass

# Supplier views
@login_required(login_url='login')
def create_supplier(request):
    forms = SupplierForm()
    if request.method == 'POST':
        forms = SupplierForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password == retype_password:
                user = User.objects.create_user(
                    username=username, password=password,
                    email=email, is_supplier=True
                )
                Supplier.objects.create(user=user, name=name, address=address)
                return redirect('supplier-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_supplier.html', context)


class SupplierListView(ListView):
    model = Supplier
    template_name = 'store/supplier_list.html'
    context_object_name = 'supplier'


# Buyer views
@login_required(login_url='login')
def create_buyer(request):
    forms = BuyerForm()
    if request.method == 'POST':
        forms = BuyerForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password == retype_password:
                user = User.objects.create_user(
                    username=username, password=password,
                    email=email, is_buyer=True
                )
                Buyer.objects.create(user=user, name=name, address=address)
                return redirect('buyer-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_buyer.html', context)


class BuyerListView(ListView):
    model = Buyer
    template_name = 'store/buyer_list.html'
    context_object_name = 'buyer'


# Season views
@login_required(login_url='login')
def create_season(request):
    forms = SeasonForm()
    if request.method == 'POST':
        forms = SeasonForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('season-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_season.html', context)


class SeasonListView(ListView):
    model = Season
    template_name = 'store/season_list.html'
    context_object_name = 'season'


# Drop views
@login_required(login_url='login')
def create_drop(request):
    forms = DropForm()
    if request.method == 'POST':
        forms = DropForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('drop-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_drop.html', context)


class DropListView(ListView):
    model = Drop
    template_name = 'store/drop_list.html'
    context_object_name = 'drop'


# Product views


# Order views
@login_required(login_url='login')
def create_order(request):
    forms = OrderForm()
    if request.method == 'POST':
        forms = OrderForm(request.POST)
        if forms.is_valid():
            supplier = forms.cleaned_data['supplier']
            product = forms.cleaned_data['product']
            design = forms.cleaned_data['design']
            color = forms.cleaned_data['color']
            buyer = forms.cleaned_data['buyer']
            season = forms.cleaned_data['season']
            drop = forms.cleaned_data['drop']
            Order.objects.create(
                supplier=supplier,
                product=product,
                design=design,
                color=color,
                buyer=buyer,
                season=season,
                drop=drop,
                status='pending'
            )
            return redirect('order-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_order.html', context)


class OrderListView(ListView):
    model = Order
    template_name = 'store/order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.all().order_by('-id')
        return context


# Delivery views
@login_required(login_url='login')
def create_delivery(request):
    forms = DeliveryForm()
    if request.method == 'POST':
        forms = DeliveryForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('delivery-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_delivery.html', context)


class DeliveryListView(ListView):
    model = Delivery
    template_name = 'store/delivery_list.html'
    context_object_name = 'delivery'

