from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("register/", UserCreateView.as_view(), name="register"),
]