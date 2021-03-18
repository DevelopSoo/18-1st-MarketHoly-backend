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
    price           = models.IntegerField()
    image_url       = models.CharField(max_length=3000)
    sales_unit      = models.CharField(max_length=30, null=True)
    amount          = models.CharField(max_length=30, null=True) # 중량/용량
    origin          = models.CharField(max_length=30, null=True)
    storage_method  = models.ForeignKey('StorageMethod', on_delete=models.SET_NULL, null=True) #DO_NOTHING ? 
    expiration_date = models.CharField(max_length=100, null=True) # 정해진 날짜가 없고 대부분 짧은 텍스트로 설명이 되어있음
    stock           = models.IntegerField()
    content         = models.TextField()
    uploaded_at     = models.DateField(auto_now_add=True)
    product_options = models.ManyToManyField('self',
                                            through='ProductOption',
                                            symmetrical=False,
                                            related_name='options') # related_name의 필요성?, symmetrical true, false의 정확한 사용, self ManyToMany
    
    class Meta:
        db_table = 'products'

class ProductOption(models.Model):
    from_product_id = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='from_product')
    to_product_id   = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='to_product')

    class Meta:
        db_table = 'product_options'

class DiscountRate(models.Model):
    product       = models.ForeignKey('Product', on_delete=models.CASCADE)
    discount_rate = models.IntegerField()

    class Meta:
        db_table = 'discount_rate'

class DailySpecialDiscount(models.Model):
    product             = models.ForeignKey('Product', on_delete=models.CASCADE)
    daily_discount_rate = models.IntegerField()
    start_date          = models.DateTimeField() # DateTimeField or DateField ? time을 같이 넘겨주거나, time은 프론트에서 처리하거나 더 나은 선택은?

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



























