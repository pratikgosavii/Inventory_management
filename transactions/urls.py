from django.urls import path

from .views import *
from store import views

urlpatterns = [


    path('add-inward/', add_inward, name='add_inward'),
    path('update-inward/<inward_id>', update_inward, name='update_inward'),
    path('delete-inward/<inward_id>', delete_inward, name='delete_inward'),
    path('list-inward/', list_inward, name='list_inward'),

    path('add-outward/', add_outward, name='add_outward'),
    path('update-outward/<outward_id>', update_outward, name='update_outward'),
    path('delete-outward/<outward_id>', delete_outward, name='delete_outward'),
    path('list-outward/', list_outward, name='list_outward'),

    path('list-stock/', list_stock, name='list_stock'),
  
]