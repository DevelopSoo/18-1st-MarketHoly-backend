from django.urls import path

from .views import RecommendView, MDRecommendView 

urlpatterns= [
    path('/recommendation', RecommendView.as_view()),
    path('/mdrecommendation', MDRecommendView.as_view())
]
