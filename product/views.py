import random
from datetime import date

from django.db.models import Q
from django.views import View
from django.http  import JsonResponse

from .models import Category, SubCategory, Product, DiscountRate, DailySpecialDiscount


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
                "name"         :product.name, 
                "price"        : product.price,
                "discount_rate": product.discount_rate.all()[0].discount_rate
                } 
                if DiscountRate.objects.filter(product=product).exists() 
                else 
                {
                "product_id"   : product_id,
                "image_url"    : product.image_url,
                "name"         : product.name,
                "price"        : product.price,
                "discount_rate": None
                } 
                for product in random_product_list]

            return JsonResponse({"listgoods": listgoods}, status=200)

        except ValueError:
            return JsonResponse({"message": "ValueError"}, status=500)

        except IndexError:
            return JsonResponse({"message": "IndexError"}, status=500)
 

#카테고리별 모든 상품들 
class ProductView(View):
    def get(self, request):
        category_id     = request.GET.get('category')
        sub_category_id = request.GET.get('sub-category')
        sort            = request.GET.get('sort')
        page            = int(request.GET.get('page', 1))

        PAGE_LIMIT = 30

        sort_keyword = {
            "new" : "-uploaded_at",
            "best": "-stock"
        }   

        # 카테고리 리스트 표출
        if category_id or sub_category_id:
            products = Product.objects.filter(Q(sub_category__category_id=category_id)|Q(sub_category_id=sub_category_id))[(page-1)*PAGE_LIMIT:page*PAGE_LIMIT]
        else:
            products = Product.objects.all().order_by(sort_keyword[sort])[(page-1)*PAGE_LIMIT:page*PAGE_LIMIT]
        
        product_list = [                   
            {
                "product_id"   : product.id,
                "name"         : product.name,
                "image_url"    : product.image_url,
                "price"        : product.price,
                "discount_rate": product.discountrate_set.get(product=product).discount_rate  
                if DiscountRate.objects.filter(product=product).exists() else None
            } for product in products
        ]

        return JsonResponse({"product_list": product_list}, status=200)


class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()

        result = [
                {
                    'id': category.id,
                    'category' : category.name,
                    'subcategories': [
                        {
                            "sub_category_id": sub_category.id,
                            "sub_category_name": sub_category.name
                        } for sub_category in SubCategory.objects.filter(category=category)
                    ]
                } for category in categories ]
        
        return JsonResponse({'result': result}, status=200)


class DailySpecialProductView(View):
    def get(self, request):
        start_date     = date.today()
        daily_products = DailySpecialDiscount.objects.filter(start_date=start_date)

        dailyspecial = [ {
                     'product_id':daily_product.product.id,
                     'name':daily_product.product.name,
                     'image_url':daily_product.product.image_url,
                     'price':daily_product.product.price,
                     'daily_discount_rate': daily_product.daily_discount_rate,
                     'start_date':start_date
                    } for daily_product in daily_products
                ]
        
        return JsonResponse({'dailyspecial': dailyspecial}, status=200)
