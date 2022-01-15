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

    path('add-return/', add_return, name='add_return'),
    path('update-return/<return_id>', update_return, name='update_return'),
    path('delete-return/<return_id>', delete_return, name='delete_return'),
    path('list-return/', list_return, name='list_return'),

    path('report-daily/', generate_report_daily, name='report_daily'),
    path('report-inward/', report_inward, name='report_inward'),
    path('report-outward/', report_outward, name='report_outward'),
    path('report-stock/', generate_report_stock, name='generate_report'),

    path('report-main/', generate_report_main, name='generate_report_main'),

    path('download', download, name='download'),

    path('delete-dashboard', delete_download, name='delete_download'),
  
]