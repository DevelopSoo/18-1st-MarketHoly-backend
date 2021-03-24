from django.urls import path

from .views import RecommendView, ProductView

urlpatterns= [
    path('/recommendation', RecommendView.as_view()),
    path('', ProductView.as_view())
]