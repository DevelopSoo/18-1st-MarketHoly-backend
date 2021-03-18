from django.db import models


class User(models.Model):
    email         = models.EmailField(max_length=45, unique=True)
    password      = models.CharField(max_length=100)
    name          = models.CharField(max_length=50)
    phone_number  = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True)
    saved_item    = models.ManyToManyField('product.Product', through='order.SavedItem') 
    
    class Meta:
        db_table = 'users'


class Address(models.Model):
    user           = models.ForeignKey('User', on_delete=models.CASCADE)
    zip_code       = models.CharField(max_length=10)
    address        = models.CharField(max_length=100)
    detail_address = models.CharField(max_length=100, null=True)
    is_default     = models.BooleanField(default=True)

    class Meta:
        db_table = 'address'


class AccumulatedMoney(models.Model):
    user             = models.ForeignKey('User', on_delete=models.CASCADE)
    product          = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True)
    order            = models.ForeignKey('order.Order', on_delete=models.SET_NULL, null=True)
    type             = models.ForeignKey('AccumulatedMoneyType', on_delete=models.SET_NULL, null=True)
    money            = models.DecimalField(max_digits=10, decimal_places=2)
    accumulated_date = models.DateField(auto_now=False, auto_now_add=False)
    expiration_date  = models.DateField(auto_now=False, auto_now_add=False) 
    is_used          = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'accumulated_money'


class AccumulatedMoneyType(models.Model):
    name   = models.CharField(max_length=15)
    reason = models.ForeignKey('AccumulatedMoneyReason', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'accumulated_money_type'


class AccumulatedMoneyReason(models.Model):
    name             = models.CharField(max_length= 45)
    money            = models.IntegerField(null=True)
    accumulated_rate = models.DecimalField(max_digits=8, decimal_places=5, null=True)

    class Meta:
        db_table = 'accumulated_money_reason'
