from django.urls import path

from product.views import CategoryView, RecommendView

urlpatterns = [
    path('/category', CategoryView.as_view()),
    path('/recommendation', RecommendView.as_view()),
]
