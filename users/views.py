from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserRegisterForm
from users.models import User


class CustomLoginView(LoginView):
    """
    Кастомное представление для входа с проверкой блокировки.
    Attributes:
        template_name (str): Путь к шаблону страницы входа.
    """

    template_name = "users/login.html"

class UserCreateView(CreateView):
    """
    Представление для регистрации нового пользователя с подтверждением по email.
    Attributes:
        model (User): Модель пользователя.
        form_class (Form): Класс формы UserRegisterForm.
        success_url (str): URL для перенаправления после успешной регистрации.
    """

    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

