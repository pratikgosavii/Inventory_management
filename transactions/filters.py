import django_filters
from django_filters import DateFilter, CharFilter
from django.forms.widgets import DateInput
from django import forms

from .models import *

class inward_filter(django_filters.FilterSet):

    company = django_filters.ModelChoiceFilter(
        queryset=company.objects.all(),
        widget=forms.Select(
            attrs={
                'class' : 'form-control',
                'id' : 'company'
            })
    )

    company_goods = django_filters.ChoiceFilter( 
                
        widget=forms.Select(attrs={'class': 'form-control', 'id' : 'company_goods'}))

    goods_company = django_filters.ChoiceFilter( 
        widget=forms.Select(attrs={'class': 'form-control', 'id' : 'goods_company'}))

    agent = django_filters.ModelChoiceFilter(
        queryset=agent.objects.all(),
        widget=forms.Select(
            attrs={
                'class' : 'form-control'
            })
    )


    DC_date_start__date = DateFilter(field_name="DC_date", lookup_expr='gte', widget=forms.DateInput(
            attrs={
                'id': 'datepicker1212',
                'type': 'date',
                'class' : 'form-control'
            }
        ))
    DC_date_end__date = DateFilter(field_name="DC_date", lookup_expr='lte', widget=forms.DateInput(
            attrs={
                'id': 'datepicker1',
                'type': 'date',
                'class' : 'form-control'
            }
        ))

    class Meta:
        model = inward
        fields = '__all__'
        exclude = ['bags', 'DC_number', 'DC_date']
       

class outward_filter(django_filters.FilterSet):

    DC_date_start__date = DateFilter(field_name="DC_date", lookup_expr='gte', widget=forms.DateInput(
            attrs={
                'id': 'datepicker1212',
                'type': 'date'
            }
        ))
    DC_date_end__date = DateFilter(field_name="DC_date", lookup_expr='lte', widget=forms.DateInput(
            attrs={
                'id': 'datepicker2321221',
                'type': 'date'
            }
        ))
    


    class Meta:
        model = outward
        fields = '__all__'
        exclude = ['bags', 'DC_number', 'DC_date']
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
            

        }

        
        
# class inward_stock(django_filters.FilterSet):
# 	DC_date__date = DateFilter(widget=DateInput(attrs={'type': 'date'}), field_name="DC_date", lookup_expr='gte')
# 	DC_date__date = DateFilter(field_name="DC_date", lookup_expr='lte')
    


# 	class Meta:
# 		model = stock
# 		fields = '__all__'
# 		exclude = ['bags', 'DC_number']