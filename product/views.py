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

            listgoods = [
                {
                "product_id"   : product.id,
                "image_url"    : product.image_url, 
                "name"         : product.name, 
                "price"        : product.price,
                "discount_rate": product.discountrate_set.get(product_id=product.id).discount_rate 
                if DiscountRate.objects.filter(product=product).exists() 
                else None
                } 
                for product in random_product_list]

            return JsonResponse({"listgoods": listgoods}, status=200)

        except ValueError:
            return JsonResponse({"message": "ValueError"}, status=500)

        except IndexError:
            return JsonResponse({"message": "IndexError"}, status=500)


# MD 추천 
class MDRecommendView(View):
    def get(self, request):
        limit       = request.GET.get('limit', 6)
        offset      = request.GET.get('offset', 6)
        category_id = int(offset)/int(limit)

        category = Category.objects.get(id=category_id)

        sub_categories        = category.subcategory_set.all()
        random_sub_categories = random.sample(list(sub_categories), 3)

        product_list_by_category = []
        for sub_category in random_sub_categories:
            two_products = sub_category.product_set.all().order_by('-stock')[:2]
            for product in two_products:
                product_info = {
                    'product_id'   : product.id,
                    "name"         : product.name,
                    "image_url"    : product.image_url,
                    "price"        : product.price,
                    "discount_rate": product.discountrate_set.get(product_id=product.id).discount_rate 
                    if DiscountRate.objects.filter(product=product).exists() 
                    else None
                }         
                
                product_list_by_category.append(product_info)

        return JsonResponse({"product_list_by_category": product_list_by_category}, status=200)


