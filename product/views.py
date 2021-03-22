import json

from django.views import View
from django.http  import JsonResponse

from product.models import Category, SubCategory


class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()

        result = []
        
        for category in categories:
            sub_categories      = SubCategory.objects.filter(category=category)
            sub_categories_list = [sub_category.name for sub_category in sub_categories]
            
            category_by_id = {}

            category_by_id['id']            = category.id
            category_by_id['category_name'] = category.name
            category_by_id['subcategories'] = sub_categories_list

            result.append(category_by_id)

        return JsonResponse({'result': result}, status=200)
