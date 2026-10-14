from django.contrib import admin

from .models import Category, Event


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sub_title", "count_events")  # overview
    list_display_links = ("id", "name")  # klickbar um auf Detailseite zu kommen
    search_fields = ("name", "sub_title")  # Suchbox sucht in name und subtitle

    @admin.display(description="Anzahl Events")
    def count_events(self, obj: Category) -> int:
        """Anzahl der Events für jede Kategorie"""
        return obj.events.count()


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "author")
    list_display_links = ("id", "name")
    search_fields = ("name", "sub_title")

    fieldsets = (
        ("Standard info", {"fields": ("name", "date", "category", "author")}),
        (
            "Detail Infos",
            {"fields": ("description", "sub_title", "is_active", "min_group")},
        ),
        # (
        #     "Tags",
        #     {"fields": ("tags",)},
        # ),
    )
