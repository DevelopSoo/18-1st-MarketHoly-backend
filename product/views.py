import random 

from django.views import View
from django.http  import JsonResponse

from .models import Category, SubCategory, Product, DiscountRate

#카테고리별 모든 상품들 
class CategoryListDetail(View):
    def get(self, request, category_id):
        category = Category.objects.get(id=category_id)
        sub_categories = category.subcategory_set.all()

        product_list = []
        for sub_category in sub_categories:
            products = sub_category.product_set.all()
            for product in products:
                    if product.to_product.all():
                        continue
                    else:
                        if DiscountRate.objects.filter(product=product).exists():
                            discount_rate = product.discountrate_set.all()[0].discount_rate
                            product_info = {
                                "id"  : product.id,
                                "name": product.name,
                                "image": product.image_url,
                                "price": product.price,
                                "discount_rate": discount_rate
                            }
                        else:
                            product_info = {
                                "id"  : product.id,
                                "name": product.name,
                                "image": product.image_url, 
                                "price":product.price
                                }
                        product_list.append(product_info)
        return JsonResponse({'product_list': product_list})