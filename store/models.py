from django.db import models

from users.models import User
from datetime import datetime, timezone

import pytz
ist = pytz.timezone('Asia/Kolkata')




class company(models.Model):

    company_name = models.CharField(max_length=120, unique=True)
    #address
    #mobile number

    
    def __str__(self):
        return self.company_name


class company_goods(models.Model):

    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='event_ticket')
    name = models.CharField(max_length=120, unique=False)
    
    
    def __str__(self):
        return self.name


class goods_company(models.Model):
    
    company_name = models.ForeignKey(company, on_delete=models.CASCADE, related_name='sfsf')
    company_goods = models.ForeignKey(company_goods , on_delete=models.CASCADE, related_name='sds')
    goods_company_name = models.CharField(max_length=120, unique=False)

    def __str__(self):
        return self.goods_company_name



class agent(models.Model):

    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='ddfdf')
    name = models.CharField(max_length=120)
    place =  models.CharField(max_length=120, unique=False)
    taluka  = models.CharField(max_length=120, unique=False)
    address = models.CharField(max_length=120, unique=False)
    district = models.CharField(max_length=120, unique=False)
    mobile_number =  models.IntegerField(unique=False)



    class Meta:
        unique_together = ('company', 'name')
        



class transport(models.Model):

    name = models.CharField(max_length=120)

    
    def __str__(self):
        return self.name