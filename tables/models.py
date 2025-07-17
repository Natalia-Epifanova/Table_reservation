from django.db import models

from users.models import User


class Table(models.Model):
    STATUS_CHOICES = [
        ("reserved", "Забронирован"),
        ("free", "Свободен"),
    ]
    table_number = models.CharField(max_length=2, verbose_name="Номер стола")
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="free",
        verbose_name="Статус бронирования стола",
    )
    number_of_seats = models.PositiveIntegerField(
        verbose_name="Количество мест за столом"
    )
    description = models.TextField(
        max_length=300, blank=True, null=True, verbose_name="Описание стола"
    )

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"

    def __str__(self):
        return f"Стол номер {self.table_number} - {self.status}"


class Reservation(models.Model):
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Стол для брони",
    )
    number_of_persons = models.PositiveIntegerField(verbose_name="Количество персон")
    date_time_of_reservation = models.DateTimeField(
        verbose_name="Дата и время бронирования"
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Владелец бронирования"
    )
    comment = models.TextField(
        max_length=300, blank=True, null=True, verbose_name="Комментарий"
    )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"Бронирование стола номер {self.table}. Дата и время: {self.date_time_of_reservation}. Пользователь: {self.owner}"
