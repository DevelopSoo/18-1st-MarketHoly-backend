import random

from django.views import View
from django.http  import JsonResponse

from .models import Category, SubCategory, Product, DiscountRate


# 현재 전체 카테고리와 전체 sub 카테고리를 대상으로 하기 때문에 
# 실제로 로직을 짤 때는 카테고리도 무작위로 12개, 
# 그리고 카테고리별 sub 카테고리는 각 1개, 
# 그 sub 카테고리의 랜덤 상품 1개
class RecommendView(View):
    def get(self, request):
        categories = Category.objects.all()
        random_categories = random.sample(list(categories), 8) # 랜덤으로 뽑을 개수. 나중에는 이 개수를 12개로 늘린다.
        
        
        # 랜덤 카테고리를 기준으로 랜덤 서브 카테고리를 1개씩 추출
        random_sub_category_list = []
        for category in random_categories:
            sub_categories = category.subcategory_set.all()
            random_sub_category = random.choice(sub_categories)
            random_sub_category_list.append(random_sub_category)
        
        # 랜덤 서브 카테고리 1개당 1개의 랜덤 상품을 추출 
        random_product_list = []
        for sub_category in random_sub_category_list:
            items = sub_category.product_set.all()
            random_product = random.choice(items)
            random_product_list.append(random_product)
        


        result = []
        for product in random_product_list:
        # 할인율이 있는 경우 없는 경우 나누기
            if product.discountrate_set.all():
                discount_rate = product.discountrate_set.all()[0].discount_rate
                product_info = {
                    "image": product.image_url,
                    "name": product.name,
                    "price": product.price,
                    "discount_rate": discount_rate
                }
            else:
                product_info = {
                    "image": product.image_url,
                    "name": product.name,
                    "price": product.price
                }

            

            result.append(product_info)
        
        return JsonResponse({"result": result}, status=200)

        # Sample larger than population or is negative
        # except ValueError:
        #     return JsonResponse({"message": "ValueError"}, status=500)

        # Cannot choose from an empty sequence
        # except IndexError:
        #     return JsonResponse({"message": "IndexError"}, status=500)