from django.urls import path

from .views import CategoryListDetail

urlpatterns= [
    path('/categorylistdetail/<int:category_id>', CategoryListDetail.as_view()), 
]
