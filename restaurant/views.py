import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, transaction
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)

from restaurant.forms import (AvailableTablesFilterForm, ContactForm,
                              ReservationForm, TableForm)
from restaurant.models import RESERVATION_DURATION, Reservation, Table


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        reservation = self.get_object()
        return reservation.owner == self.request.user

    def handle_no_permission(self):
        raise PermissionDenied("Вы не являетесь владельцем этого бронирования")


class HomeView(FormView):
    template_name = "restaurant/home.html"
    form_class = ContactForm
    success_url = reverse_lazy("restaurant:home")

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        phone = form.cleaned_data.get("phone", "не указан")
        message = form.cleaned_data["message"]
        print(f"Получено сообщение от {name} (телефон: {phone}): {message}")
        return super().form_valid(form)


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

    def get_success_url(self):
        return reverse_lazy(
            "restaurant:reservation_detail", kwargs={"pk": self.object.pk}
        )

    def get_initial(self):
        initial = super().get_initial()
        if "table_id" in self.request.GET:
            initial["table"] = self.request.GET["table_id"]
        if "date" in self.request.GET:
            initial["date_of_reservation"] = self.request.GET["date"]
        elif "date_of_reservation" in self.request.GET:
            initial["date_of_reservation"] = self.request.GET["date_of_reservation"]
        if "time" in self.request.GET:
            initial["time_of_reservation"] = self.request.GET["time"]
        elif "time_of_reservation" in self.request.GET:
            initial["time_of_reservation"] = self.request.GET["time_of_reservation"]
        if "persons" in self.request.GET:
            initial["number_of_persons"] = self.request.GET["persons"]
        elif "number_of_persons" in self.request.GET:
            initial["number_of_persons"] = self.request.GET["number_of_persons"]
        return initial

    @transaction.atomic
    def form_valid(self, form):
        try:
            form.instance.owner = self.request.user
            response = super().form_valid(form)
            return response
        except IntegrityError as e:
            if "unique_reservation" in str(e):
                form.add_error(
                    None,
                    "Этот стол на данное время уже занят. Пожалуйста, выберите другой стол или время.",
                )
            else:
                form.add_error(
                    None,
                    "Произошла ошибка при бронировании. Пожалуйста, попробуйте еще раз.",
                )
            return self.form_invalid(form)


class ReservationUpdateView(OwnerRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm

    def get_success_url(self):
        return reverse_lazy("users:profile_detail", kwargs={"pk": self.request.user.pk})


class ReservationDetailView(OwnerRequiredMixin, LoginRequiredMixin, DetailView):
    model = Reservation


class ReservationDeleteView(OwnerRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Reservation

    def get_success_url(self):
        return reverse_lazy("users:profile_detail", kwargs={"pk": self.request.user.pk})


class ReservationListView(OwnerRequiredMixin, LoginRequiredMixin, ListView):
    model = Reservation
    success_url = reverse_lazy("restaurant:home")
    context_object_name = "reservations"


class AvailableTablesListView(ListView):
    model = Table
    template_name = "restaurant/available_tables.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = AvailableTablesFilterForm(self.request.GET or None)
        context["filter_form"] = form

        if self.request.GET and not form.is_valid():
            context["form_invalid"] = True
            context["form_errors"] = form.errors

        return context

    def get_queryset(self):
        form = AvailableTablesFilterForm(self.request.GET or None)
        queryset = Table.objects.all()

        if form.is_valid():
            date = form.cleaned_data["date_of_reservation"]
            time = form.cleaned_data["time_of_reservation"]
            persons = form.cleaned_data["number_of_persons"]

            queryset = queryset.filter(number_of_seats__gte=persons)

            start_time = datetime.datetime.combine(date, time)
            end_time = start_time + RESERVATION_DURATION

            reservations = Reservation.objects.filter(date_of_reservation=date)

            reserved_tables = []
            for reservation in reservations:
                reservation_start = datetime.datetime.combine(
                    date, reservation.time_of_reservation
                )
                reservation_end = reservation_start + RESERVATION_DURATION

                if not (reservation_end <= start_time or reservation_start >= end_time):
                    reserved_tables.append(reservation.table_id)

            queryset = queryset.exclude(id__in=reserved_tables)
        else:
            queryset = queryset.none()

        return queryset
