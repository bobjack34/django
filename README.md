# Event Manager

Ein Django-Beispielprojekt zur Entwicklung einer klassischen Webanwendung mit Events, Kategorien, Benutzern, Formularen, Tests und Deployment.

## Voraussetzungen

Für das Projekt wird [uv](https://docs.astral.sh/uv/) zur Verwaltung von Python und den Abhängigkeiten verwendet.

Installation von `uv` unter Windows mit PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Installation überprüfen:

```powershell
uv --version
```

## Projekt lokal einrichten

Repository klonen und in das Django-Projekt wechseln:

```powershell
git clone <repository-url>
cd event_project
cd app
```

Das Repository enthält eine `env_example`. Diese muss für die lokale Entwicklung in `.env` umbenannt bzw. kopiert werden.


```bash
cp env_example .env
```

Die Werte in `.env` anschließend bei Bedarf anpassen.

Wichtig: Die `.env` enthält lokale Konfiguration und Secrets und darf nicht ins Git-Repository eingecheckt werden.

## Python und Dependencies installieren

Das Projekt verwendet `uv`. Dadurch ist keine manuelle Erstellung oder Aktivierung eines Virtual Environments notwendig.

Die benötigte Python-Version installieren:

```bash
uv python install
```

Alle Dependencies aus `pyproject.toml` und `uv.lock` installieren:

```bash
uv sync
```

Python-Version kontrollieren:

```bash
uv run python --version
```

## Datenbank vorbereiten

Migrationen ausführen:

```bash
uv run manage.py migrate
```

Optional einen Admin-Benutzer erstellen:

```bash
uv run python manage.py createsuperuser
```

## Development Server starten

```bash
uv run manage.py runserver
```

Danach ist die Anwendung normalerweise unter `http://127.0.0.1:8000/` erreichbar.

## Django Management Commands

Einige häufig benötigte Befehle:

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py shell
uv run python manage.py collectstatic
```

Alle verfügbaren Commands anzeigen:

```bash
uv run manage.py help
```

## Tests

Das Projekt verwendet `pytest` und `pytest-django`.

Alle Tests:

```bash
uv run pytest
```

Ausführlicher:

```bash
uv run pytest -v
```

Nur die Tests der Events-App:

```bash
uv run pytest tests/events
```

Die Tests befinden sich außerhalb der Django-Apps:

```text
tests/
├── conftest.py
└── events/
    ├── test_views.py
```

Gemeinsam verwendete Fixtures werden in `conftest.py` definiert.

## Projektstruktur

Vereinfacht:

```text
event_project/
├── compose.yaml
├── .env
├── env_example
│
└── app/
    ├── manage.py
    ├── pyproject.toml
    ├── uv.lock
    │
    ├── events/
    │   ├── models.py
    │   ├── views.py
    │   ├── forms.py
    │   ├── urls.py
    │   ├── validators.py
    │   ├── factories.py
    │   └── services.py
    │
    ├── users/
    │
    ├── templates/
    ├── static/
    │
    └── tests/
        ├── conftest.py
        └── events/
```

## Architektur

Das Projekt demonstriert unter anderem:

```text
Browser
   │
   ▼
urls.py
   │
   ▼
View
   │
   ├── Form
   │
   ├── Service
   │
   ▼
Model / ORM
   │
   ▼
Datenbank
```

Views sollten primär HTTP-spezifische Aufgaben übernehmen. Umfangreichere Geschäftslogik kann in einen Service Layer ausgelagert werden.

## Django ORM

Beispiele:

```python
Event.objects.all()

Event.objects.filter(is_active=True)

Event.objects.filter(name__icontains="python")

Event.objects.select_related("category", "author")
```

QuerySets sind grundsätzlich lazy. Django führt die SQL-Abfrage normalerweise erst aus, wenn die Daten tatsächlich benötigt werden.

## Formulare

Für Model-basierte Formulare werden `ModelForm`-Klassen verwendet.

Feldspezifische Validierung:

```python
def clean_sub_title(self): ...
```

Validierung mehrerer voneinander abhängiger Felder:

```python
def clean(self): ...
```

Der typische Ablauf eines POST-Requests ist:

```text
POST
 ↓
Form(request.POST)
 ↓
is_valid()
 ↓
cleaned_data
 ↓
save()
 ↓
Redirect
```

## Authentifizierung und Berechtigungen

Views, die nur für angemeldete Benutzer verfügbar sein sollen, können beispielsweise `LoginRequiredMixin` verwenden.

Objektbezogene Berechtigungen können mit `UserPassesTestMixin` geprüft werden.

Beispiel:

```python
class HasPermissionToEditMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.get_object().author == self.request.user
```

Damit kann beispielsweise sichergestellt werden, dass nur der Autor eines Events dieses bearbeiten darf.

## Static Files

Während der Entwicklung übernimmt Django die Bereitstellung statischer Dateien.

Im Template:

```django
{% load static %}

<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

Für ein Production-Deployment werden die Dateien gesammelt:

```powershell
uv run python manage.py collectstatic --noinput
```

Im Projekt wird WhiteNoise verwendet, um statische Dateien in Production auszuliefern.

## Production Check

Django besitzt einen eingebauten Deployment-Check:

```bash
uv run manage.py check --deploy
```

Dieser sollte vor einem Deployment ausgeführt werden.

Unter anderem sollten in Production folgende Punkte beachtet werden:

```text
DEBUG=False
SECRET_KEY nicht im Repository
ALLOWED_HOSTS konfigurieren
HTTPS verwenden
Static Files sammeln
Migrationen ausführen
Production Server statt runserver verwenden
```

## Weiterführende Dokumentation

### Django

[Django Heroes](https://djangoheroes.org/)

[Django Documentation](https://docs.djangoproject.com/)

[Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)

[Django Models](https://docs.djangoproject.com/en/stable/topics/db/models/)

[Django QuerySets](https://docs.djangoproject.com/en/stable/topics/db/queries/)

[Django Forms](https://docs.djangoproject.com/en/stable/topics/forms/)

[Django Authentication](https://docs.djangoproject.com/en/stable/topics/auth/)

[Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)

[Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

### Class-Based Views

[Classy Class-Based Views](https://ccbv.co.uk/)

Sehr hilfreiche Referenz zum Nachschlagen der Django Class-Based Views, ihrer Methoden und Vererbung.

### Python und uv

[uv Documentation](https://docs.astral.sh/uv/)

### Testing

[pytest Documentation](https://docs.pytest.org/)

[pytest-django Documentation](https://pytest-django.readthedocs.io/)

[Factory Boy Documentation](https://factoryboy.readthedocs.io/)

### Weitere verwendete Werkzeuge

[Django Extensions](https://django-extensions.readthedocs.io/)

[django-stubs](https://github.com/typeddjango/django-stubs)

[WhiteNoise](https://whitenoise.readthedocs.io/en/latest/)

[Mermaid Live Editor](https://mermaid.live/)

## Hinweise

`manage.py runserver` ist ausschließlich für die Entwicklung gedacht.

Für Production sollte ein geeigneter WSGI- oder ASGI-Server verwendet werden, beispielsweise Uvicorn:

```bash
uv run uvicorn config.asgi:application --host 0.0.0.0 --port 8000
```

Die konkrete Konfiguration hängt von der Deployment-Umgebung ab.