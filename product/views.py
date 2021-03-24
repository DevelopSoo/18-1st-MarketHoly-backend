import random

from django.db.models import Q
from django.http      import JsonResponse
from django.views     import View

from product.models import Category, SubCategory, Product, DiscountRate 


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

<<<<<<< HEAD

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


=======
>>>>>>> main
class DetailProductView(View):
    def get(self, request, product_id):
    
        exist_product = Product.objects.filter(id=product_id).exists()
        if not exist_product:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXIST'}, status=400)

        product = Product.objects.get(id=product_id)
        
        have_discount = DiscountRate.objects.filter(product=product).exists()
        if have_discount:
            discount      = DiscountRate.objects.get(product=product)
            discount_rate = discount.discount_rate
        else:
            discount_rate = None
        
        info = {
            'id': product_id,
            'name': product.name,
            'description': product.description,
            'image_url': product.image_url,
            'price': product.price,
            'stock': product.stock,
            'content': product.content,
            'uploaded_at': product.uploaded_at,
            'sales_unit': product.sales_unit if product.sales_unit else [],
            'amount': product.amount if product.amount else [],
            'origin': product.origin if product.origin else [],
            'storage_method': product.storage_method.name if product.storage_method else [],
            'expiration_date': product.expiration_date if product.expiration_date else [],
            'discount_rate': discount_rate
        }

        sub_category     = Product.objects.get(id=product_id).sub_category
        products         = Product.objects.filter(sub_category=sub_category)
        random_products  = random.sample(list(products), 3)
        related_products = [{'id': product.id,
                              'name': product.name,
                              'image_url': product.image_url,
                              'price': product.price
                              } for product in random_products]
        
<<<<<<< HEAD
        return JsonResponse({'info': info, 'related_products': related_products}, status=200)
=======
        return JsonResponse({'info': info, 'related_products': related_products}, status=200)
>>>>>>> main
