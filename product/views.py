import json

from django.http  import JsonResponse
from django.views import View

from product.models import Product, DiscountRate 

class DetailProductView(View):
    def post(self, request):
        try:
            data       = json.loads(request.body) 
            product_id = data['product_id']

            exist_product = Product.objects.filter(id=product_id).exists()
            if not exist_product:
                return JsonResponse({'message': 'NO_PRODUCT'}, status=400)

            product = Product.objects.get(id=product_id)
            
            name            = product.name
            description     = product.description
            image_url       = product.image_url
            price           = product.price
            stock           = product.stock
            content         = product.content
            uploaded_at     = product.uploaded_at
            sales_unit      = product.sales_unit if product.sales_unit else []
            amount          = product.amount if product.amount else []
            origin          = product.origin if product.origin else []
            expiration_date = product.expiration_date if product.expiration_date else []
            storage_method  = product.storage_method.name if product.storage_method else []
            
            have_discount = DiscountRate.objects.filter(product=product).exists()
            if have_discount:
                discount      = DiscountRate.objects.get(product=product)
                discount_rate = discount.discount_rate
            else:
                discount_rate = []
            
            info = {
                'name': name,
                'description': description,
                'image_url': image_url,
                'price': price,
                'stock': stock,
                'content': content,
                'uploaded_at': uploaded_at,
                'sales_unit': sales_unit,
                'amount': amount,
                'origin': origin,
                'storage_method': storage_method,
                'expiration_date': expiration_date,
                'discount_rate': discount_rate,
            }

            return JsonResponse(info, status=200)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSONDecodeError'}, status=400) 
        
        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)
