import json

from django.http  import JsonResponse
from django.views import View

from product.models import Product, DiscountRate 

class DetailProductView(View):
    def get(self, request):
        
        product_id    = request.GET['id']
        exist_product = Product.objects.filter(id=product_id).exists()
        if not exist_product:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXIST'}, status=400)

        product = Product.objects.get(id=product_id)
        
        have_discount = DiscountRate.objects.filter(product=product).exists()
        if have_discount:
            discount      = DiscountRate.objects.get(product=product)
            discount_rate = discount.discount_rate
        else:
            discount_rate = []
        
        info = {
            'name': product.name,
            'description': product.description,
            'image_url': product.image_url,
            'price': product.price,
            'stock': product.stock,
            'content': product.content,
            'uploaded_at': product.uploaded_at,
            'sales_unit': product.sales_unit if product.sales_unit else [],
            'amount': product.amount if product.amount else [],
            'origin': product.origin if product.origin else [],
            'storage_method': product.storage_method.name if product.storage_method else [],
            'expiration_date': product.expiration_date if product.expiration_date else [],
            'discount_rate': discount_rate,
        }

        return JsonResponse(info, status=200)
