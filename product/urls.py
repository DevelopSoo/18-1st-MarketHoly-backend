from django.urls import path

from .views import BestListView

urlpatterns= [
    path('/bestlist', BestListView.as_view())
]