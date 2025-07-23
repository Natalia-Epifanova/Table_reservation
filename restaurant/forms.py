import datetime

from django.core.exceptions import ValidationError
from django.forms import (DateField, DateInput, Form, IntegerField, ModelForm,
                          Textarea, TimeField, TimeInput)

from restaurant.models import RESERVATION_DURATION, Reservation, Table


class StyleFormMixin:
    """
    Миксин для стилизации форм. Добавляет CSS-класс 'form-control' ко всем полям формы.
    Methods:
        __init__: Инициализирует форму и добавляет CSS-классы ко всем полям.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class TableForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Table
        fields = "__all__"

    def clean_table_number(self):
        table_number = self.cleaned_data["table_number"]
        query = Table.objects.filter(table_number=table_number)

        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)

        if query.exists():
            raise ValidationError("Стол с таким номером уже существует")

        return table_number


class ReservationForm(StyleFormMixin, ModelForm):
    date_of_reservation = DateField(
        widget=DateInput(attrs={"type": "date", "class": "form-control"}),
        label="Дата бронирования",
    )
    time_of_reservation = TimeField(
        widget=TimeInput(attrs={"type": "time", "class": "form-control"}),
        label="Время бронирования",
    )

    class Meta:
        model = Reservation
        exclude = ["owner"]
        widgets = {
            "comment": Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        time = cleaned_data.get("time_of_reservation")
        date = cleaned_data.get("date_of_reservation")
        persons = cleaned_data.get("number_of_persons")
        table = cleaned_data.get("table")

        if time and (time < datetime.time(11, 0) or time > datetime.time(22, 30)):
            raise ValidationError("Ресторан работает с 11:00 до 23:00")

        if date and date < datetime.date.today():
            raise ValidationError("Нельзя забронировать стол на прошедшую дату")

        if table and persons and persons > table.number_of_seats:
            raise ValidationError(
                f"Выбранный стол вмещает только {table.number_of_seats} персон(ы). "
                f"Пожалуйста, выберите другой стол или уменьшите количество гостей."
            )

        if table and date and time:
            start_time = datetime.datetime.combine(date, time)
            end_time = start_time + RESERVATION_DURATION

            existing_reservations = Reservation.objects.filter(
                table=table, date_of_reservation=date
            ).exclude(pk=self.instance.pk if self.instance else None)

            for reservation in existing_reservations:
                existing_start = datetime.datetime.combine(
                    reservation.date_of_reservation, reservation.time_of_reservation
                )
                existing_end = existing_start + RESERVATION_DURATION

                if (start_time < existing_end) and (end_time > existing_start):
                    raise ValidationError(
                        f"Стол уже забронирован с {reservation.time_of_reservation.strftime('%H:%M')} "
                        f"до {(existing_start + datetime.timedelta(hours=2)).time().strftime('%H:%M')}. "
                        f"Пожалуйста, выберите другое время или другой стол."
                    )
        return cleaned_data


class AvailableTablesFilterForm(StyleFormMixin, Form):
    date_of_reservation = DateField(
        widget=DateInput(attrs={"type": "date"}),
        label="Дата бронирования",
        initial=datetime.date.today,
    )
    time_of_reservation = TimeField(
        widget=TimeInput(attrs={"type": "time"}),
        label="Время бронирования",
        initial=datetime.time(11, 0),
    )
    number_of_persons = IntegerField(label="Количество персон", min_value=1)
