from django.db import models

#from user.models    import User
#from product.models import Product
#from order.models   import Order

class Review(models.Model):
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product    = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    order      = models.ForeignKey('order.Order', on_delete=models.CASCADE) # order status에 따라서 리뷰 작성 가능 여부가 결정되는데, order_id값으로 delete속성 어떻게 정해야 할지 모르겠음
    image_url  = models.CharField(max_length=2000, null=True)
    content    = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'reviews'

class ReviewLike(models.Model):
    user     = models.ForeignKey('user.User', on_delete=models.CASCADE)
    review   = models.ForeignKey('Review', on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'review_likes'


