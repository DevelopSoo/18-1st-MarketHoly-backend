from django.urls import path

from .views import RecommendView, CategoryListDetail

urlpatterns= [
    path('/recommendation', RecommendView.as_view()),
    path('/categorylistdetail', CategoryListDetail.as_view())
]