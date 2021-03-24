import random 

from django.views import View
from django.http  import JsonResponse

from .models import Category, SubCategory, Product, DiscountRate

#카테고리별 모든 상품들 
class CategoryListDetail(View):
    def get(self, request):
        category_id     = request.GET.get('category')
        sub_category_id = request.GET.get('sub-category')
        sort            = request.GET.get('sort')

        
        # 카테고리 리스트 표출
        if category_id:
            category       = Category.objects.get(id=category_id)
            sub_categories = category.subcategory_set.all()

            product_list = []
            for sub_category in sub_categories:
                products = sub_category.product_set.all()
                for product in products:
                    product_info = {
                        "id"  : product.id,
                        "name": product.name,
                        "image_url": product.image_url,
                        "price": product.price,
                        "discount_rate": product.discountrate_set.get(product=product).discount_rate 
                        if DiscountRate.objects.filter(product=product).exists() 
                        else None
                    }

                    product_list.append(product_info)

            return JsonResponse({"product_list": product_list}, status=200)
        
        # 서브 카테고리 리스트 표출
        elif sub_category_id:
            sub_category = SubCategory.objects.get(id=sub_category_id)
            products     = sub_category.product_set.all()

            product_list = []

            for product in products:
                product_info = {
                    "id": product.id,
                    "name": product.name,
                    "image_url": product.image_url,
                    "price": product.price,
                    "discount_rate": 
                    if DiscountRate.objects.filter(product=product).exists() 
                    else None
                }

                product_list.append(product_info)
            
            return JsonResponse({"product_list": product_list}, status=200)

        # 신상품 리스트 표출
        elif sort == "new":
            products = Product.objects.all().order_by('-uploaded_at')

            new_product = []

            for product in products:
                product_info = {
                    "id": product.id,
                    "name": product.name,
                    "image_url": product.image_url,
                    "price": product.price,
                    "discount_rate": 
                    if DiscountRate.objects.filter(product=product).exists() 
                    else None
                }

                new_product.append(product_info)      

            return JsonResponse({"new_product": new_product}, status=200)          
        
        # 베스트 리스트 표출
        elif sort == "best":
            products = Product.objects.all().order_by('-stock')

            best_products = []

            for product in products:
                product_info = {
                    "id": product.id,
                    "name": product.name,
                    "image_url": product.image_url,
                    "price": product.price,
                    "discount_rate": 
                    if DiscountRate.objects.filter(product=product).exists() 
                    else None
                }
                best_products.append(product_info) 

            return JsonResponse({"best_products": best_products}, status=200)                
 