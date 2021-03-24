import json

from django.views import View
from django.http  import JsonResponse

from product.models import Category, SubCategory


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
