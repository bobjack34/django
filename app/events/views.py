from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from events.services.booking_management import CancelException, cancel_event

from .forms import CategoryForm, EventForm
from .models import Category, Event


@login_required
def event_cancel(request: HttpRequest, pk: int):
    """einen Event absagen."""
    event = get_object_or_404(Event, pk=pk)

    try:
        cancel_event(event, request.user)
    except CancelException as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, str(e))
    else:
        messages.success(request, "Event wurde erfolgreich gecancelt")

    return redirect("events:event_detail", pk=pk)


class HasPermissionToEditMixin(UserPassesTestMixin):
    """Prüft, ob ein user der Author des Events ist."""

    def test_func(self) -> bool:
        return any(
            [
                self.get_object().author == self.request.user,
                self.request.user.groups.filter(name="Moderatoren").exists(),
            ]
        )


class EventDeleteView(HasPermissionToEditMixin, DeleteView):
    """Deleteview löscht ein Objekt.

    der generische Templatename ist event_confirm_delete.html

    event/3/delete
    """

    model = Event
    # in Klassen immer reverse_lazy nutzen, da vorher die Route nicht bekannt ist
    success_url = reverse_lazy("events:event_list")


class EventUpdateView(HasPermissionToEditMixin, UpdateView):
    """Updateview editiert ein Objekt.

    der generische Templatename ist event_form.html

    events/3/update
    """

    model = Event
    form_class = EventForm

    def get_success_url(self) -> str:
        return reverse("events:event_detail", args=[self.object.pk])


class EventCreateView(LoginRequiredMixin, CreateView):
    """Createview erstellt ein Objekt.

    der generische Templatename ist event_form.html

    events/create
    """

    model = Event
    form_class = EventForm
    # success_url = "events:event_list"

    def get_success_url(self) -> str:
        """erzeugt dynamisch die URL für die Weiterleitung nach dem erfolgreichen Erzeugen eines
        Objekts (redirect after post)"""
        # reverse erzeugt via dem Path und dem arg die eigentliche finale URL (events/3)
        return reverse("events:event_detail", args=[self.object.pk])

    def form_valid(self, form):
        """Wird ausgeführt, wenn das Formular valide ist."""
        # set current logged in user as author of new event
        form.instance.author = self.request.user
        return super().form_valid(form)


class EventDetailView(DetailView):
    """Generische Detailview stellt ein Objekt als Detailseite dar.

    in den urls muss der Platzhalter "pk" lauten.
    der generische Templatename ist event_detail.html

    events/3
    """

    model = Event


class EventListView(ListView):
    """Generische ListView stellt Events als Liste dar.
    generischer Templatename modelname_list.html
    im Template ist der Kontext object_list
    """

    model = Event
    # queryset = Event.objtext.all()

    def get_queryset(self) -> QuerySet[Any, Any]:
        print(f"Request Object GET: {self.request.GET}")

        # select_related macht einen INNER JOIN
        qs = Event.objects.select_related("category", "author").filter(is_active=True)
        query = self.request.GET.get("q")

        if query:
            qs = qs.filter(name__icontains=query)

        return qs


def category_create(request: HttpRequest) -> HttpResponse:
    """Anlegen einer neuen Kategorie.

    events/categories/create
    """
    if request.method == "POST":
        form = CategoryForm(request.POST)
        # hier wird die Kategorie in die DB eingetragen (wenn valide)
        if form.is_valid():
            category = form.save()
            return redirect("events:category_detail", pk=category.pk)
    else:
        # im GET Zwei zeigen wir dem user ein leeres Formular an
        form = CategoryForm()

    return render(
        request,
        "events/category_form.html",
        {
            "form": form,
        },
    )


def category_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Anzeigen einer spezifischen Kategorie.

    Erhebe 404 Fehler falls die id nicht existiert.

    events/categories/3
    """
    category = get_object_or_404(Category, pk=pk)
    return render(
        request,
        "events/category_detail.html",
        {
            "category": category,
            "value": 42,
        },
    )


def category_list(request: HttpRequest) -> HttpResponse:
    """Auflistung der Kategorien.

    events/categories
    """
    categories = Category.objects.filter(is_active=True)

    return render(
        request,
        "events/category_list.html",
        {
            "categories": categories,
        },
    )


def hello(request: HttpRequest) -> HttpResponse:
    print("Hello, World")  # auf Console
    return HttpResponse("hello world")  # im Browser
