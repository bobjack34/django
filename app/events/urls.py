from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    # events/hello
    path("hello", views.hello, name="hello"),
    path("categories", views.category_list, name="category_list"),
    path("categories/<int:pk>", views.category_detail, name="category_detail"),
    path("categories/create", views.category_create, name="category_create"),
    # Urls für Events: /events
    path("", views.EventListView.as_view(), name="event_list"),
    path("create", views.EventCreateView.as_view(), name="event_create"),
    path("<int:pk>", views.EventDetailView.as_view(), name="event_detail"),
    path("<int:pk>/update", views.EventUpdateView.as_view(), name="event_update"),
    path("<int:pk>/delete", views.EventDeleteView.as_view(), name="event_delete"),
    path("<int:pk>/cancel", views.event_cancel, name="event_cancel"),
]
