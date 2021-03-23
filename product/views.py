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
            product_list_by_category = [
                    {"name": product.name,
                    "image": product.image_url,
                    "price": product.price,
                    "discount_rate": product.discountrate_set.all()[0].discount_rate}
                    if DiscountRate.objects.filter(product=product).exists() 
                    else 
                    {"name": product.name,
                    "image": product.image_url,
                    "price": product.price,
                    "discount_rate": None}
                    for product in two_products]
        return JsonResponse({"product_list_by_category": product_list_by_category}, status=200)
