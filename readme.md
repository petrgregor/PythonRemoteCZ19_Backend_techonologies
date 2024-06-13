# Django

## Instalace
```bash
python -m pip install django==4.1.1
```

## Vytvoření Django projektu
```bash
django-admin startproject hollymovies .
```

Ideálně i s tečkou na konci, aby projekt nebyl zbytečně vznořený.

- Základní struktura projektu (hollymovies)
  - settings.py - zde je veškeré nastavení projektu
  - urls.py - zde jsou uvedeny url adresy na které budou navázané funkce

## Spuštění serveru

Defaultně na portu 8000: 
```bash
python manage.py runserver
```

Port můžeme změnit parametrem: 
```bash
python manage.py runserver 8001
```

## Vytvoření aplikace

viewer = název aplikace
```bash
python manage.py startapp viewer
```

Vznikla nová složka s názvem viewer, která obsahuje:
- migrations - složka, která bude obsahovat migrační skripty (neupravovat)
- admin.py - zde budeme ragistrovat modely, které chceme zobrazit v administrační části projektu
- apps.py - nastavení aplikace (není potřeba měnit)
- models.py - zde budou definované modely (schéma databáze)
- tests.py - zde uvádíme testy
- views.py - zde bude naprogramovaná funkcionalita aplikace

## Registrace aplikace do Djanga

V souboru ./hollymovies/settings.py přidáme aplikaci viewwer do seznamu INSTALLED_APPS.

## Migrace databáze

Vytvoříme migrační skript:
```bash
python manage.py makemigrations
```

Provedeme změny v databázi:
```bash
python manage.py migrate
```

## Shell

```bash
python manage.py shell
```

```bash
from viewer.models import Genre
Genre.objects.all()
```

## Administration 

```bash
python manage.py createsuperuser
```

-> zaregistrovat modely do admin.py

## DUMP/LOAD

Export databáze:
```bash
python manage.py dumpdata viewer --output fixtures.json
```

Import databáze:
```bash
python manage.py loaddata fixtures.json
```

POZOR: Nefunguje to s diakritikou.

Nainstalujeme rozšíření:
```bash
pip install django-dump-load-utf8
```

Přidáme řádek
'django_dump_load_utf8',
do INSTALLED_APPS v settings.py.

```bash
python manage.py dumpdatautf8 viewer --output fixtures.json
```

```bash
python manage.py loaddatautf8 .\fixtures.json
```

## Queries

### .get()
Vrací jednu instanci nalezeného záznamu v databázi. 

### .filter()
Vrací kolekci instancí nalezených záznamů.

`Movie.objects.filter(title="The Green Mile")`

`Movie.objects.filter(rating=5)`

`Movie.objects.filter(rating__gt=4)`   `__gt` => "větší než" 

`Movie.objects.filter(rating__gte=4)`  `__gte` => "větší rovno"

`Movie.objects.filter(rating__lt=4)`   `__lt` => "menší než"

`Movie.objects.filter(rating__lte=4)`  `__lte` => menší rovno

`drama = Genre.objects.get(name='Drama')`

`Movie.objects.filter(genre=drama)`

`Movie.objects.filter(genre__name="Drama")`

`Movie.objects.filter(released__year=1994)`

`Movie.objects.filter(title__contains="Gump")`

`Movie.objects.filter(title__in=['Se7en', 'Fight Club'])`  # „Se7en” and „Fight Club”

`Movie.objects.exclude(released__year=1994)`

`Movie.objects.filter(title="Avatar").exists()` -- test, zda existuje nějaký záznam

`Movie.objects.exclude(released__year=1994).count()` -- vrátí počet vyhovujícíh záznamů

`Movie.objects.all().order_by('released')` -- uspořádáme dle data natočení vzestupně

`Movie.objects.all().order_by('-released')` -- sestupně

## Data manipulation

### CREATE
`Genre.objects.create(name='Documentary')`

```python
genre = Genre(name='Comedy')
genre.save()
```

### UPDATE 

`Movie.objects.filter(released__year=2000).update(rating=5)`

```python
pulp_fiction = Movie.objects.get(title='Pulp Fiction')
pulp_fiction.rating = 7
pulp_fiction.save()
```

### DELETE
```python
Movie.objects.filter(title__contains='Godfather').delete()
```

## Add another
https://django-addanother.readthedocs.io/en/latest/

`pip install django_addanother`

Do `settings.py` vložit do INSTALLED_APPS: 'django_addanother',

Do `views.pyv do formuláře do podtřídy `Meta` přidáme widget:
```
widgets = {
            'directors': AddAnotherWidgetWrapper(
                SelectMultiple,
                reverse_lazy('creator_create')
            )
        }
```

Do template form_movie.html přidáme:
`{% load static %}`

a do formuláře:
```
<script src="{% static 'admin/js/vendor/jquery/jquery.js' %}"></script>
{{ form.media }}
```

Do view `PeopleCreateView(CreatePopupMixin, CreateView):` přidáme `CreatePopupMixin`

Do šablony base.html přidáme: 
```
{% if not view.is_popup %}
...
{% endif %}
```

# Vygenerování ER diagramu
- stáhnout Graphiz: https://graphviz.org/download/
- nainstalovat `pip install graphviz`
- nainstalovat `pip install django-extensions`
- vložit 'django_extensions' do settings.py od INSTALLED_APPS
- do settings.py přidat nastavení grafu:
```python
GRAPH_MODELS = {
  'all_applications': True,
  'graph_models': True,
}
```
- nainstalovat `pip install pyparsing pydot`
- spustíme příkaz `python manage.py graph_models -a > erd.dot`
- spustíme příkaz `python manage.py graph_models --pydot -a -g -o erd.png`

## Testy
V každé aplikaci máme soubor `tests.py`, do kterého můžeme vkládat testy.
Je možné vytvořit další soubory s testy, název by měl ideálně začínat `test*.py`.

Příkaz pro testování je: `python manage.py test` spustí všechny testy v souborech začínající `test`.

Příkaz pro testování `python manage.py test viewer.test_models` spustí všechny testy v souboru 
`test_models.py` v aplikaci `viewer`.

Základní testy se spouští na virtuální databázi, která má stejné schéma, jako naše definovaná 
databáze v `models.py`, ale je prázdná a nezávislá na skutečné databázi.

## Rady a tipy pro finální projekt

- všichni v týmu musí mít stejnou verzi Djanga (i ostatních balíčků)
- vytvořit readme.md soubor s popisem projektu, 
může obsahovat i obrázky (ER diagram, screenshoty,...)
- vytvořit git repozitář a sdílet v týmu (settings -> Collaborators)
- uložit si seznam nainstalovaných/potřebných balíčků:
  ```bash
  pip freeze > requirements.txt
  ```
- výsledné stránky (ne tamplates) otestovat, zda jsou validní: https://validator.w3.org/nu/#textarea

