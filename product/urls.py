from django.urls import path

from .views import MDRecommendView

urlpatterns= [
    path('/mdrecommendation', MDRecommendView.as_view()),
]
