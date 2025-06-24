Fullstack Project - Jakub Boruch

Opis projektu

Jest to pełnostackowa aplikacja webowa napisana w Pythonie z wykorzystaniem frameworka Flask. Projekt zawiera funkcjonalności:

Formularz rejestracyjny dla użytkowników

Galerię zdjęć

Panel administracyjny do zarządzania użytkownikami

Podstawowy system logowania administratora

Projekt jest podzielony na backend (Flask, SQLite) oraz frontend (HTML, CSS, JavaScript).

Technologie

Python 3.x

Flask

SQLite (lokalna baza danych)

HTML5

CSS3

JavaScript

Struktura katalogu

Fullstack-project/
├── backend.py          # Główny plik backendu Flask
├── instance/users.db   # Lokalna baza danych SQLite
├── static/             # Statyczne pliki frontendowe (JS, CSS, obrazy)
├── templates/          # Szablony HTML
└── .venv/              # (opcjonalnie) Środowisko wirtualne Pythona

Wymagania

Przed uruchomieniem projektu zalecane jest utworzenie środowiska wirtualnego:

python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows

Następnie zainstaluj wymagane biblioteki:

pip install Flask

Uruchomienie projektu

Upewnij się, że znajdujesz się w katalogu Fullstack-project/

Uruchom backend Flask:

python backend.py

Aplikacja będzie dostępna pod adresem http://127.0.0.1:5000/

Funkcjonalności

Strona główna z formularzem rejestracyjnym dla użytkowników.

Galeria zdjęć dostępna dla wszystkich użytkowników.

Panel administracyjny zabezpieczony logowaniem administratora (hasło w kodzie backendu).

Możliwość edycji i usuwania użytkowników przez admina.

Uwagi

Domyślna baza danych users.db znajduje się w katalogu instance/. W razie potrzeby można ją usunąć, aby wygenerować czystą bazę przy pierwszym uruchomieniu.

Wszystkie dane logowania administratora są na sztywno wpisane w kodzie backend.py (dla celów edukacyjnych, w realnym projekcie należy je przechowywać bezpiecznie!).
