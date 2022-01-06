from django.urls import path

from .views import *
from store import views

urlpatterns = [

    path('get-company_goods-ajax/', get_company_goods_ajax, name="get_company_goods_ajax"),
    path('get-goods_company-ajax/', get_goods_company_ajax, name="get_goods_company_ajax"),

    path('add-company/', add_company, name='add_company'),
    path('update-company/<company_id>', update_company, name='update_company'),
    path('delete-company/<company_id>', delete_company, name='delete_company'),
    path('list-company/', list_company, name='list_company'),

    path('add-company-goods/', add_company_goods, name='add_company_goods'),
    path('update-company-goods/<company_goods_id>', update_company_goods, name='update_company_goods'),
    path('delete-company-goods/<company_goods_id>', delete_company_goods, name='delete_company_goods'),
    path('list-company-goods/', list_company_goods, name='list_company_goods'),

    
    path('goods-company/', add_goods_company, name='add_goods_company'),
    path('update-goods-company/<company_goods_id>', update_goods_company, name='update_goods_company'),
    path('delete-goods-company/<company_goods_id>', delete_goods_company, name='delete_goods_company'),
    path('list-goods-company/', list_goods_company, name='list_goods_company'),

    path('add-agent/', add_agent, name='add_agent'),
    path('update-agent/<agent_id>', update_agent, name='update_agent'),
    path('delete-agent/<agent_id>', delete_agent, name='delete_agent'),
    path('list-agent/', list_agent, name='list_agent'),


    path('create-brand/', create_brand, name='create-brand'),
    path('brand-list/', BrandListView.as_view(), name='brand-list'),
    path('update-delete/', update_brand, name='delete_brand'),
    path('brand-delete/', delete_brand, name='delete_brand'),

    path('view-product/<brand_id>', views.list_product, name='view-product'),
    path('add-product/', views.add_product, name='add-product'),
    path('update-product/<id>', views.update_product, name='update_product'),
    path('delete-product/<id>', views.delete_product, name='delete-product'),


    # 
    # 
    # 
    # 
    # 



    path('create-supplier/', create_supplier, name='create-supplier'),
    path('create-buyer/', create_buyer, name='create-buyer'),
    path('create-season/', create_season, name='create-season'),
    path('create-drop/', create_drop, name='create-drop'),

    
    # path('add-product/', views.add_products, name='add-product'),

    path('create-order/', create_order, name='create-order'),
    path('create-delivery/', create_delivery, name='create-delivery'),

    path('supplier-list/', SupplierListView.as_view(), name='supplier-list'),
    path('buyer-list/', BuyerListView.as_view(), name='buyer-list'),
    path('season-list/', SeasonListView.as_view(), name='season-list'),
    path('drop-list/', DropListView.as_view(), name='drop-list'),
    path('order-list/', OrderListView.as_view(), name='order-list'),
    path('delivery-list/', DeliveryListView.as_view(), name='delivery-list'),
]
