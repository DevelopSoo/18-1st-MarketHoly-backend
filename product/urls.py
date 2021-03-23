from django.urls import path

from .views import NewListView

urlpatterns= [
    path('/newlist', NewListView.as_view()),
]