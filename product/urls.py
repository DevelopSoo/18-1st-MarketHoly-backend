from django.urls import path

from product.views import DetailProductView

urlpatterns = [
        path('/detail/<int:product_id>', DetailProductView.as_view()),
]
