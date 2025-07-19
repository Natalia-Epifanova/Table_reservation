from django import forms
from django.core.exceptions import ValidationError

from restaurant.models import Table


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = "__all__"

    def clean_table_number(self):
        table_number = self.cleaned_data['table_number']
        query = Table.objects.filter(table_number=table_number)

        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)

        if query.exists():
            raise ValidationError("Стол с таким номером уже существует")

        return table_number