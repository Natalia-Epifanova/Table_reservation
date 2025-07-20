from django.contrib import admin

from restaurant.models import Reservation, Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):

    list_display = ("id", "table_number", "status", "number_of_seats", "description")
    search_fields = ("table_number", "number_of_seats")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "table",
        "number_of_persons",
        "date_of_reservation",
        "time_of_reservation",
        "owner",
    )
    search_fields = ("table", "date_of_reservation", "time_of_reservation")
