import random 

from django.views import View
from django.http  import JsonResponse

from .models import *


class MDRecommendView(View):
    def get(self, request):
        limit = request.GET['limit']
        offset = request.GET['offset']
        category_id = offset/limit

        category = Category.objects.get(id=category_id)

        sub_categories = category.subcategory_set.all()
        random_sub_categories = random.sample(list(sub_categories), 3)

        product_list_by_category = []
        for sub_category in random_sub_categories:
            two_products = sub_category.product_set.all().order_by('-stock')[:2]
            for product in two_products:
                if DiscountRate.objects.filter(product=product).exists():
                    discount_rate = product.discount_rate.all()[0].discount_rate
                    product_dict = {
                        "name": product.name,
                        "image": product.image_url,
                        "price": product.price,
                        "discount_rate": discount_rate
                    }
                else:
                    product_dict = {
                        "name": product.name,
                        "image": product.image_url,
                        "price": product.price,
                    }

                product_list_by_category.append(product_dict)
                # product_list_by_category = [if DiscountRate.objects.filter(product=product).exists() for product in products]
        return JsonResponse({"product_list_by_category": product_list_by_category}, status=200)
