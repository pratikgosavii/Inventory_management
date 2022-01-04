from django.urls import path

from .views import *
from store import views

urlpatterns = [


    path('add-inward/', add_inward, name='add_inward'),
    path('list-inward/', list_inward, name='list_inward'),

    path('add-outward/', add_outward, name='add_outward'),
    path('list-outward/', list_outward, name='list_outward'),
    

]