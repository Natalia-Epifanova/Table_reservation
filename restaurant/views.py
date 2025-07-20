from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
)

from restaurant.forms import ReservationForm, TableForm
from restaurant.models import Reservation, Table


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        reservation = self.get_object()
        return reservation.owner == self.request.user

    def handle_no_permission(self):
        raise PermissionDenied("Вы не являетесь владельцем этого бронирования")


class HomeView(TemplateView):
    template_name = "restaurant/home.html"


class RestaurantInfoView(TemplateView):
    template_name = "restaurant/restaurant_info.html"


class TableCreateView(UserPassesTestMixin, CreateView):
    model = Table
    form_class = TableForm
    template_name = "restaurant/table_form.html"
    success_url = reverse_lazy("restaurant:home")

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        raise PermissionDenied("У вас нет прав для создания столов")


class TableUpdateView(UserPassesTestMixin, UpdateView):
    model = Table
    form_class = TableForm
    template_name = "restaurant/table_form.html"
    success_url = reverse_lazy("restaurant:home")

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        raise PermissionDenied("У вас нет прав для обновления информации у столов")


class TableDeleteView(UserPassesTestMixin, DeleteView):
    model = Table
    success_url = reverse_lazy("restaurant:home")

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        raise PermissionDenied("У вас нет прав для удаления столов")


class ReservationCreateView(LoginRequiredMixin, CreateView):

    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy("restaurant:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ReservationUpdateView(OwnerRequiredMixin, LoginRequiredMixin, UpdateView):

    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy("restaurant:home")


class ReservationDetailView(OwnerRequiredMixin, LoginRequiredMixin, DetailView):

    model = Reservation


class ReservationDeleteView(OwnerRequiredMixin, LoginRequiredMixin, DeleteView):

    model = Reservation
    success_url = reverse_lazy("restaurant:home")
