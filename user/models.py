from django.db import models

#from product.models import Product
#from order.models   import Order

class User(models.Model):
    email         = models.EmailField(max_length=45, unique=True)
    password      = models.CharField(max_length=100)
    name          = models.CharField(max_length=50)
    phone_number  = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True)
    saved_item    = models.ManyToManyField('product.Product') # migrate하고 shell에서 related_name 정하기
    
    class Meta:
        db_table = 'users'

class Address(models.Model):
    user           = models.ForeignKey('User', on_delete=models.CASCADE)
    zip_code       = models.IntegerField()
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
    money            = models.DecimalField(max_digits=8, decimal_places=3)
    accumulated_date = models.DateField(auto_now=False, auto_now_add=False)
    expiration_date  = models.DateField(auto_now=False, auto_now_add=False) # accumulated_date 를 기준으로 일년 뒤 해당 월의 말일 까지 
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
    accumulated_rate = models.DecimalField(max_digits=2, decimal_places=1, null=True)

    class Meta:
        db_table = 'accumulated_money_reason'


