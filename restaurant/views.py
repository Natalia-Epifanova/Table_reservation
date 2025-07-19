from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView

from restaurant.forms import TableForm
from restaurant.models import Table


class HomeView(TemplateView):

    template_name = "restaurant/home.html"


class TableCreateView(UserPassesTestMixin, CreateView):
    model = Table
    form_class = TableForm
    template_name = 'table_form.html'
    success_url = '/restaurant/'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        raise PermissionDenied("У вас нет прав для создания столов")

class TableUpdateView(UserPassesTestMixin, UpdateView):
    model = Table
    form_class = TableForm
    template_name = 'table_form.html'
    success_url = '/restaurant/'

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