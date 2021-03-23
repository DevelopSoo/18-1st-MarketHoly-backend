from django.urls import path

from .views import MDRecommendView, CategoryListDetail, SubCategoryListDetail, BestListView, NewListView

urlpatterns= [
    path('/mdrecommendation', MDRecommendView.as_view()),
]
