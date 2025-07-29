import datetime

from django.db import models

from users.models import User

RESERVATION_DURATION = datetime.timedelta(hours=2)


class Table(models.Model):

    table_number = models.IntegerField(unique=True, verbose_name="Номер стола")
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
        return f"Стол номер {self.table_number} (максимальное количество персон - {self.number_of_seats})"


class Reservation(models.Model):
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Стол для брони",
    )
    number_of_persons = models.PositiveIntegerField(verbose_name="Количество персон")
    date_of_reservation = models.DateField(
        default=datetime.date.today, verbose_name="Дата бронирования"
    )
    time_of_reservation = models.TimeField(
        default=datetime.time(11, 0), verbose_name="Время бронирования"
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
        constraints = [
            models.UniqueConstraint(
                fields=["table", "date_of_reservation", "time_of_reservation"],
                name="unique_reservation",
            )
        ]

    def __str__(self):
        return (
            f"Бронирование стола номер {self.table}. Дата: {self.date_of_reservation}, "
            f"Время: {self.time_of_reservation}. Пользователь: {self.owner}"
        )
