from django.urls import path

from product.views import CategoryView, RecommendView, ProductView

urlpatterns = [
    path('/category', CategoryView.as_view()),
    path('/recommendation', RecommendView.as_view()),
    path('', ProductView.as_view()),
]
