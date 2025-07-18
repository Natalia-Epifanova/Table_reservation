from django.urls import path

from restaurant.apps import TablesConfig
from restaurant.views import HomeView

app_name = TablesConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
