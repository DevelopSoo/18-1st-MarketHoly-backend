from django.db import models

#from user.models    import User
#from product.models import Product

class Order(models.Model):
    user           = models.ForeignKey('user.User', on_delete=models.CASCADE)
    order_status   = models.ForeignKey('OrderStatus', on_delete=models.SET_NULL, null=True) # on_delete 속성
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, null=True)
    price          = models.DecimalField(max_digits=8, decimal_places=2)
    order_number   = models.CharField(max_length=60) # 차후 수정 가능
    purchase_time  = models.DateTimeField(auto_now=True)
    cart           = models.ManyToManyField('product.Product', through='Cart') # migrate후 shell 에서 작성

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'order_status'

class SavedItem(models.Model):
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'saved_items'

class Cart(models.Model):
    order    = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='cart_order')
    product  = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'carts'

class PaymentMethod(models.Model):
    method = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'payment_method'

