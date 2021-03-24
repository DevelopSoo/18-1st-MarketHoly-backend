from django.urls import path

from order.views import AddToCartView, CartListView, OrderView

urlpatterns = [
    path('', OrderView.as_view()),
    path('/cart', AddToCartView.as_view()), # query parameter
    path('/cartlist', CartListView.as_view()),
]
