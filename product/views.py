import json

from django.views import View
from django.http  import JsonResponse

from product.models import Category, SubCategory


class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()

        result = [{'id': category.id,
                   'category' : category.name,
                   'subcategories': sub_category.name} for category in categories
                   for sub_category in SubCategory.objects.filter(category=category)]

        return JsonResponse({'result': result}, status=200)
