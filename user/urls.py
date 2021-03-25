from django.urls import path, include

from user.views import SignUpView, LoginView, NameView


urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/login', LoginView.as_view()),
    path('/name', NameView.as_view()),
]
