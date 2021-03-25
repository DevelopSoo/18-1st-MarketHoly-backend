from django.urls import path

from order.views import CartView, OrderView

urlpatterns = [
    path('', OrderView.as_view()),
    path('/cart', CartView.as_view()),
]
