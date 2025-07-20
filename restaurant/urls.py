from django.urls import path

from restaurant.apps import TablesConfig
from restaurant.views import (
    HomeView,
    ReservationCreateView,
    ReservationDeleteView,
    ReservationDetailView,
    ReservationUpdateView,
    RestaurantInfoView,
    TableCreateView,
    TableDeleteView,
    TableUpdateView,
)

app_name = TablesConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("restaurant_info/", RestaurantInfoView.as_view(), name="restaurant_info"),
    path("table/create/", TableCreateView.as_view(), name="table_create"),
    path("table/<int:pk>/update/", TableUpdateView.as_view(), name="table_update"),
    path("table/<int:pk>/delete/", TableDeleteView.as_view(), name="table_delete"),
    path(
        "reservation/create/",
        ReservationCreateView.as_view(),
        name="reservation_create",
    ),
    path(
        "reservation/<int:pk>/update/",
        ReservationUpdateView.as_view(),
        name="reservation_update",
    ),
    path(
        "reservation/<int:pk>/delete/",
        ReservationDeleteView.as_view(),
        name="reservation_delete",
    ),
    path(
        "reservation/<int:pk>/",
        ReservationDetailView.as_view(),
        name="reservation_detail",
    ),
]
