import random 

from django.views import View
from django.http  import JsonResponse

from .models import Product, DiscountRate


class BestListView(View):
    def get(self, request):
        products = Product.objects.all().order_by('stock')

        best_products = []

        for product in products:
            if product.to_product.all():
                continue
            else:              
                if DiscountRate.objects.filter(product=product).exists():
                    discount_rate = product.discountrate_set.all()[0].discount_rate
                    product_info  = {
                        "image_url"    : product.image_url,
                        "name"         : product.name,
                        "price"        : product.price,
                        "discount_rate": discount_rate
                    }
                else:
                    product_info = {
                        "image_url": product.image_url,
                        "name"     : product.name,
                        "price"    : product.price
                    }

                best_products.append(product_info)
        
        return JsonResponse({"best_products": best_products})