from django.contrib import admin

from .models import *


class SupplierAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'address', 'created_date']


class BuyerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'address', 'created_date']


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Season)
admin.site.register(Drop)
admin.site.register(Brand)
admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(Brand_Product)
admin.site.register(company_goods)
