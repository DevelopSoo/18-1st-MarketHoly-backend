from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'


class SubCategory(models.Model):
    name     = models.CharField(max_length=30)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'


class Product(models.Model):
    sub_category    = models.ForeignKey('SubCategory', on_delete=models.PROTECT)
    name            = models.CharField(max_length=45)
    description     = models.CharField(max_length=60)
    price           = models.DecimalField(max_digits=10, decimal_places=2)
    image_url       = models.CharField(max_length=3000)
    sales_unit      = models.CharField(max_length=30, null=True)
    amount          = models.CharField(max_length=30, null=True) 
    origin          = models.CharField(max_length=30, null=True)
    storage_method  = models.ForeignKey('StorageMethod', on_delete=models.SET_NULL, null=True)  
    expiration_date = models.CharField(max_length=100, null=True) 
    stock           = models.PositiveIntegerField(default=0)
    content         = models.TextField()
    uploaded_at     = models.DateField(auto_now_add=True)
    product_options = models.ManyToManyField('self',
                                            through='ProductOption',
                                            symmetrical=False,
                                            related_name='options') 
    
    class Meta:
        db_table = 'products'


class ProductOption(models.Model):
    from_product_id = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='from_product')
    to_product_id   = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='to_product')

    class Meta:
        db_table = 'product_options'


class DiscountRate(models.Model):
    product       = models.ForeignKey('Product', on_delete=models.CASCADE)
    discount_rate = models.DecimalField(max_digits=10, decimal_places=5)

    class Meta:
        db_table = 'discount_rate'


class DailySpecialDiscount(models.Model):
    product             = models.ForeignKey('Product', on_delete=models.CASCADE)
    daily_discount_rate = models.DecimalField(max_digits=10, decimal_places=5)
    start_date          = models.DateField()

    class Meta:
        db_table = 'daily_special_discount'


class Allergy(models.Model):
    name = models.CharField(max_length=45)
    product_allergy = models.ManyToManyField('Product')

    class Meta:
        db_table = 'allergies'


class StorageMethod(models.Model):
    name = models.CharField(max_length=8)

    class Meta:
        db_table = 'storage_methods'


class Review(models.Model):
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product    = models.ForeignKey('Product', on_delete=models.CASCADE)
    order      = models.ForeignKey('order.Order', on_delete=models.CASCADE) 
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
