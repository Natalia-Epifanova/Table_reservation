from django.contrib import admin

from restaurant.models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Table.

    Attributes:
        list_display (tuple): Поля, отображаемые в списке объектов.
        search_fields (tuple): Поля, по которым выполняется поиск.
    """

    list_display = ("table_number", "status", "number_of_seats", "description")
    search_fields = ("table_number", "number_of_seats")

