from django.urls import path

from product.views import DetailProductView

urlpatterns = [
    path('/detail', DetailProductView.as_view()),
]
