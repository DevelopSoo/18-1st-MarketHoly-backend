import random

from django.views import View
from django.http  import JsonResponse

from .models import Category, SubCategory, Product, DiscountRate


# 이 상품 어때요?
class RecommendView(View):
    def get(self, request):
        try:
            categories        = Category.objects.all()
            random_categories = random.sample(list(categories), 8)

            random_sub_category_list = [random.choice(category.subcategory_set.all()) for category in random_categories]
            random_product_list      = [random.choice(sub_category.product_set.all()) for sub_category in random_sub_category_list]

            listgoods = []
            for product in random_product_list:

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

                listgoods.append(product_info)
            
            return JsonResponse({"listgoods": listgoods}, status=200)

        except ValueError:
            return JsonResponse({"message": "ValueError"}, status=500)

        except IndexError:
            return JsonResponse({"message": "IndexError"}, status=500)


