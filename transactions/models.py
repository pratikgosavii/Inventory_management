from django.db import models

# Create your models here.



from users.models import User
from datetime import datetime, timezone
from store.models import *


class agent(models.Model):

    name = models.CharField(max_length=120, unique=True)
    taluka  = models.CharField(max_length=120, unique=True)
    district = models.CharField(max_length=120, unique=True)
    mobile_number =  models.IntegerField()


class inward(models.Model):

    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='sdwe')
    company_goods = models.ForeignKey(company_goods , on_delete=models.CASCADE, related_name='wfgv')
    goods_company = models.ForeignKey(goods_company , on_delete=models.CASCADE, related_name='xvc')
    agent = models.ForeignKey(agent , on_delete=models.CASCADE, related_name='sdv')
    bags = models.IntegerField()
    DC_number = models.IntegerField()
    DC_date = models.DateTimeField()


class outward(models.Model):

    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='fgv')
    company_goods = models.ForeignKey(company_goods , on_delete=models.CASCADE, related_name='fd')
    goods_company = models.ForeignKey(goods_company , on_delete=models.CASCADE, related_name='cvg')
    agent = models.ForeignKey(agent , on_delete=models.CASCADE, related_name='df')
    bags = models.IntegerField()
    DC_number = models.IntegerField()
    DC_date = models.DateTimeField()

    

