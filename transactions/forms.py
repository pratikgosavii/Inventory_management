from django import forms
from django.forms.widgets import DateTimeInput

from .models import *
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime



class inward_Form(forms.ModelForm):
    class Meta:
        model = inward
        fields = '__all__'
        widgets = {
            'company': forms.Select(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'company_goods': forms.Select(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'goods_company': forms.Select(attrs={
                'class': 'form-control', 'id': 'pck_size'
            }),
             'agent': forms.Select(attrs={
                'class': 'form-control', 'id': 'total_pck'
            }),
            'bags': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'bag_size'
            }),
            'DC_number': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'total_bag'
            }),

            'DC_date': DateTimeInput(attrs={ 'class': 'form-control', 'type': 'datetime-local'}, format = '%Y-%m-%dT%H:%M'),
            
        }



class outward_Form(forms.ModelForm):
    class Meta:
        model = outward
        fields = '__all__'
        widgets = {
            'company': forms.Select(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'company_goods': forms.Select(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'goods_company': forms.Select(attrs={
                'class': 'form-control', 'id': 'pck_size'
            }),
             'agent': forms.Select(attrs={
                'class': 'form-control', 'id': 'total_pck'
            }),
            'bags': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'bag_size'
            }),
            'DC_number': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'total_bag'
            }),

            'DC_date': DateTimeInput(attrs={ 'class': 'form-control', 'type': 'datetime-local'}, format = '%Y-%m-%dT%H:%M'),
            
        }



class goods_company_Form(forms.ModelForm):
    class Meta:
        model = stock
        fields = '__all__'
        widgets = {
             'company': forms.Select(attrs={
                'class': 'form-control', 'id': 'company'
            }),

            'company_goods': forms.Select(attrs={
                'class': 'form-control', 'id': 'company_goods'
            }),
           
            'goods_company_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),

            'total_bag': forms.NumberInput(attrs={
                'class': 'form-control cal', 'id': 'total_bag'
            }),
           
            
        }
