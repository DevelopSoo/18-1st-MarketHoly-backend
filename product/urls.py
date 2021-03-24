from django.urls import path

from product.views import CategoryView, RecommendView, ProductView, DetailProductView

urlpatterns = [
    path('/category', CategoryView.as_view()),
    path('/recommendation', RecommendView.as_view()), 
    path('/detail/<int:product_id>', DetailProductView.as_view()),
    path('', ProductView.as_view()),
]
