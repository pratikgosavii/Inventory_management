from django.db import models

from users.models import User
from datetime import datetime, timezone

import pytz
ist = pytz.timezone('Asia/Kolkata')




class company(models.Model):

    company_name = models.CharField(max_length=120, unique=True)
    #address
    #mobile number


class company_goods(models.Model):

    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='event_ticket')
    name = models.CharField(max_length=120, unique=True)
    pck_size = models.IntegerField()
    total_pck = models.IntegerField()
    bag_size = models.IntegerField()
    total_bag = models.IntegerField()


class goods_company(models.Model):

    company_goods = models.ForeignKey(company_goods , on_delete=models.CASCADE, related_name='sds')
    company_name = models.CharField(max_length=120, unique=True)



class Brand(models.Model):

    goods_company = models.ForeignKey(goods_company , on_delete=models.CASCADE, related_name='sd')
    name = models.CharField(max_length=120, unique=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name



class Brand_Product(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    date_time = models.DateTimeField()
   


    def __str__(self):
        return self.name


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Drop(models.Model):
    name = models.CharField(max_length=120, unique=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('decline', 'Decline'),
        ('approved', 'Approved'),
        ('processing', 'Processing'),
        ('complete', 'Complete'),
        ('bulk', 'Bulk'),
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Brand, on_delete=models.CASCADE)
    design = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True)
    drop = models.ForeignKey(Drop, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    courier_name = models.CharField(max_length=120)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.courier_name

