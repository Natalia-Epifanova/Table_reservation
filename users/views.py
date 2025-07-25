import datetime

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from restaurant.models import Reservation
from users.forms import UserProfileForm, UserRegisterForm
from users.models import User


class CustomLoginView(LoginView):
    template_name = "users/login.html"


class UserCreateView(CreateView):

    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")


class UserUpdateView(UpdateView):

    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("restaurant:home")


class UserDetailView(DetailView):
    model = User
    template_name = "users/profile_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.date.today()
        now = datetime.datetime.now().time()

        reservations = Reservation.objects.filter(owner=self.request.user).order_by(
            "date_of_reservation", "time_of_reservation"
        )

        past_reservations = reservations.filter(
            date_of_reservation__lt=today
        ) | reservations.filter(date_of_reservation=today, time_of_reservation__lt=now)

        upcoming_reservations = reservations.filter(
            date_of_reservation__gt=today
        ) | reservations.filter(date_of_reservation=today, time_of_reservation__gte=now)

        context.update(
            {
                "past_reservations": past_reservations,
                "upcoming_reservations": upcoming_reservations,
            }
        )
        return context
