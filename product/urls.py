from django.urls import path

from .views import RecommendView

urlpatterns = [
    path('/recommendation', RecommendView.as_view())
]
