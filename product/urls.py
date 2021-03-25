from django.urls import path

from product.views import RecommendView, MDRecommendView, CategoryView, ProductView, DetailProductView, DailySpecialProductView



urlpatterns= [
    path('/category', CategoryView.as_view()),
    path('/dailyspecial', DailySpecialProductView.as_view()),
    path('/mdrecommendation', MDRecommendView.as_view()),
    path('/recommendation', RecommendView.as_view()), 
    path('/detail/<int:product_id>', DetailProductView.as_view()),
    path('', ProductView.as_view()),
]
