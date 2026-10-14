"""
Formulare für die Events-App
"""

from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ("author", "is_active")

        widgets = {  # noqa: RUF012
            "date": forms.DateInput(
                format=("%Y-%m-%d %H:%M"), attrs={"type": "datetime-local"}
            ),
        }

    def clean_sub_title(self) -> str | None:
        """Der Rückgabewert ist der WErt, der in der DB für sub_title eingetragen wird.

        Validierung: Prüfen, ob ein * enthalten ist, und wenn ja, einen Fehler auslösen
        """
        sub_title = self.cleaned_data["sub_title"]
        if isinstance(sub_title, str) and "*" in sub_title:
            raise ValidationError("Im Sub-Title darf kein * enthalten sein!")
        return sub_title

    def clean(self) -> dict:
        """Crossfield Validierungen gehen über diese Funtion. clean wird nach allen
        anderen Validierungen aufgerufen."""
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        min_group = cleaned_data.get("min_group")

        if category and category.name == "Music" and min_group > 5:
            self.add_error("category", "falsche Mingroup für Musik")
            self.add_error("min_group", "Teilnehmerzahl prüfen")

            raise ValidationError(
                "In der Kategorie Musik dürfen nicht mehr als 5 Teilnehmer sein."
            )

        return cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        # fields = (
        #     "name",
        #     "sub_title",
        #     "description",
        #     "is_active",
        # )
        fields = "__all__"
