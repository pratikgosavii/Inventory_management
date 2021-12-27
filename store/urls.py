from django.urls import path

from .views import *
from store import views

urlpatterns = [


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
