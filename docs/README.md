# Platforma testów językowych

Aplikacja Django do tworzenia i zarządzania testami do nauki języków.

## Funkcjonalności
- Wiele typów testów:
  - Wypełnianie luk z pamięci (TEXT_INPUT_MEMORY)
  - Wypełnianie luk z listy słów (TEXT_INPUT_WORDLIST)
  - Test jednokrotnego wyboru (SINGLE_CHOICE)
  - Test wielokrotnego wyboru (MULTIPLE_CHOICE)
  - Test z lukami i wyborem odpowiedzi (CHOICE_WITH_GAPS)
- Automatyczne parsowanie testów z tekstu
- Podgląd i walidacja testów
- Kategoryzacja testów za pomocą tagów
- Obsługa różnych formatów odpowiedzi (A., a), 1), -)
- Automatyczna standaryzacja formatów
- Walidacja poprawności struktury testów
- Zarządzanie testami poprzez intuicyjny interfejs

## Wymagania techniczne
- Python 3.11 lub nowszy
- Django 4.2 LTS
- Bulma 0.9.4 (przez npm)
- Node.js i npm do zarządzania zależnościami front-end
- Dart Sass do kompilacji SCSS

## Szybki start
1. Sklonuj repozytorium:
```bash
git clone [adres_repozytorium]
cd [nazwa_katalogu]
```

2. Utwórz środowisko wirtualne:
```bash
python -m venv venv
source venv/bin/activate  # (Linux/Mac) 
# lub
venv\Scripts\activate     # (Windows)
```

3. Zainstaluj zależności:
```bash
pip install -r requirements.txt
npm install  # dla zależności front-end
```

4. Skonfiguruj środowisko:
```bash
cp .env.example .env  # skopiuj przykładowy plik konfiguracyjny
# edytuj .env według potrzeb
```

5. Wykonaj migracje:
```bash
python manage.py migrate
```

6. Uruchom serwer deweloperski:
```bash
python manage.py runserver
```

## Struktura projektu
```
.
├── docs/                 # Dokumentacja projektu
├── lang_quiz/           # Główny moduł projektu Django
└── quiz_builder/        # Aplikacja do budowania testów
```

## Dokumentacja
Szczegółowa dokumentacja znajduje się w katalogu `docs/`:
- `development.md` - dokumentacja dla deweloperów
- `TODO.md` - planowane funkcjonalności
- Katalog `api/` - dokumentacja API

## Aktualizacje i zmiany
Informacje o zmianach w projekcie znajdują się w pliku `CHANGELOG.md`