from django.urls import path

from .views import *
from store import views

urlpatterns = [

    path('get-company_goods-ajax/', get_company_goods_ajax, name="get_company_goods_ajax"),
    path('get-goods_company-ajax/', get_goods_company_ajax, name="get_goods_company_ajax"),
    path('get-agent_company-ajax/', get_agent_company_ajax, name="get_agent_company_ajax"),

    path('add-company/', add_company, name='add_company'),
    path('update-company/<company_id>', update_company, name='update_company'),
    path('delete-company/<company_id>', delete_company, name='delete_company'),
    path('list-company/', list_company, name='list_company'),

    path('add-company-goods/', add_company_goods, name='add_company_goods'),
    path('update-company-goods/<company_goods_id>', update_company_goods, name='update_company_goods'),
    path('delete-company-goods/<company_goods_id>', delete_company_goods, name='delete_company_goods'),
    path('list-company-goods/', list_company_goods, name='list_company_goods'),

    
    path('add-goods-company/', add_goods_company, name='add_goods_company'),
    path('update-goods-company/<company_goods_id>', update_goods_company, name='update_goods_company'),
    path('delete-goods-company/<company_goods_id>', delete_goods_company, name='delete_goods_company'),
    path('list-goods-company/', list_goods_company, name='list_goods_company'),

    path('add-agent/', add_agent, name='add_agent'),
    path('update-agent/<agent_id>', update_agent, name='update_agent'),
    path('delete-agent/<agent_id>', delete_agent, name='delete_agent'),
    path('list-agent/', list_agent, name='list_agent'),

    #delete urls 

    path('list-company-delete/', list_company_delete, name='list_company_delete'),
    path('list-company-goods-delete/', list_company_goods_delete, name='list_company_goods_delete'),
    path('list-goods-company-delete/', list_goods_company_delete, name='list_goods_company_delete'),
    path('list-agent-delete/', list_agent_delete, name='list_agent_delete'),






    # 
    # 
    # 
    # 
    # 

]
