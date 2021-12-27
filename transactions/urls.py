from django.urls import path

from .views import *
from store import views

urlpatterns = [


    path('create-brand/', index, name='create-brand'),
    

]