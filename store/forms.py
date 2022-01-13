from django import forms

from .models import *
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime


class company_Form(forms.ModelForm):
    class Meta:
        model = company
        fields = ['company_name']
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            
        }


class company_goods_Form(forms.ModelForm):
    class Meta:
        model = company_goods
        fields = '__all__'
        widgets = {
            'company': forms.Select(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'pck_size': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'pck_size'
            }),
            
            'bag_size': forms.NumberInput(attrs={
                'class': 'form-control cal', 'id': 'bag_size'
            }),
           
     
            
        }




class goods_company_Form(forms.ModelForm):
    class Meta:
        model = goods_company
        fields = '__all__'
        widgets = {
            'company_goods': forms.Select(attrs={
                'class': 'form-control', 'id': 'company_goods'
            }),
            'company_name': forms.Select(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'goods_company_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
           
            
        }




class agent_Form(forms.ModelForm):
    class Meta:
        model = agent
        fields = '__all__'
        widgets = {
            'company': forms.Select(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'taluka': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'taluka'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'taluka'
            }),
            'place': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'mobile_number'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'district'
            }),
            'mobile_number': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'mobile_number'
            }),
            

        }
           