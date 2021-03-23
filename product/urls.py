from django.urls import path

from .views import MDRecommendView, CategoryListDetail, SubCategoryListDetail, BestListView, NewListView

urlpatterns= [
    path('/mdrecommendation/<int:category_id>', MDRecommendView.as_view()),
]