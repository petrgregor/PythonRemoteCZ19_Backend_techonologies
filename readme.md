# Django

## Instalace
```python
python -m pip install django==4.1.1
```

## Vytvoření Django projektu
```python
django-admin startproject hollymovies .
```

Ideálně i s tečkou na konci, aby projekt nebyl zbytečně vznořený.

- Základní struktura projektu (hollymovies)
  - settings.py - zde je veškeré nastavení projektu
  - urls.py - zde jsou uvedeny url adresy na které budou navázané funkce

## Spuštění serveru

Defaultně na portu 8000: 
```python
python manage.py runserver
```

Port můžeme změnit parametrem: 
```python
python manage.py runserver 8001
```

## Vytvoření aplikace

viewer = název aplikace
```python
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
```python
python manage.py makemigrations
```

Provedeme změny v databázi:
```python
python manage.py migrate
```

## Shell

```python
python manage.py shell
```

```shell
from viewer.models import Genre
Genre.objects.all()
```

## Administration 

```python
python manage.py createsuperuser
```

-> zaregistrovat modely do admin.py

## DUMP/LOAD

Export databáze:
```python
python manage.py dumpdata viewer --output fixtures.json
```

Import databáze:
```python
python manage.py loaddata fixtures.json
```

POZOR: Nefunguje to s diakritikou.

Nainstalujeme rozšíření:
```bash
pip install django-dump-load_utf8
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

## Rady a tipy pro finální projekt

- všichni v týmu musí mít stejnou verzi Djanga (i ostatních balíčků)
- vytvořit readme.md soubor s popisem projektu, 
může obsahovat i obrázky (ER diagram, screenshoty,...)
- vytvořit git repozitář a sdílet v týmu (settings -> Collaborators)
- uložit si seznam nainstalovaných/potřebných balíčků:
  ```bash
  pip freeze > requirements.txt
  ```
