from django.urls import path

from restaurant.apps import TablesConfig
from restaurant.views import HomeView, TableCreateView, TableUpdateView

app_name = TablesConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("table/create/", TableCreateView.as_view(), name="table_create"),
    path("table/<int:pk>/update/", TableUpdateView.as_view(), name="table_update"),
    path("table/<int:pk>/delete/", TableUpdateView.as_view(), name="table_delete"),
]
