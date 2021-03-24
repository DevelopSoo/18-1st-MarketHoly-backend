from django.urls import path

from .views import CategoryListDetail

urlpatterns= [
    path('/categorylistdetail', CategoryListDetail.as_view()),
]
