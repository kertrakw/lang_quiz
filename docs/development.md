# Dokumentacja deweloperska

## Wymagania środowiskowe i konfiguracja

### Wymagane technologie
- Python 3.11 lub nowszy (wymagany dla nowych funkcji asyncio i typing)
- Django 4.2 LTS (długoterminowe wsparcie, stabilność API)
- Bulma 0.9.4 (przez npm, nowoczesny framework CSS)
- Node.js i npm (zarządzanie zależnościami front-end)

### Przygotowanie środowiska deweloperskiego
```bash
# Tworzenie wirtualnego środowiska
python -m venv venv

# Aktywacja środowiska
source venv/bin/activate  # (Linux/Mac) 
# lub
venv\Scripts\activate     # (Windows)

# Instalacja zależności
pip install -r requirements.txt
```

## Standardy kodowania i nazewnictwo

### Zasady ogólne
- Komentarze w kodzie piszemy po polsku (dla lepszego zrozumienia przez zespół)
- Interfejs użytkownika (teksty, komunikaty) po angielsku
- Nazwy zmiennych, funkcji, klas po angielsku
- Docstringi po polsku (dokumentacja funkcji i klas)
- Zgodność z PEP 8 (standard formatowania kodu Python)

### Przykład prawidłowego formatowania kodu:
```python
def validate_test_structure(content: str) -> bool:
    """
    Sprawdza poprawność struktury testu.
    
    Walidacja obejmuje:
    - Format luk (czy używany jest [ _ ])
    - Obecność odpowiedzi w nawiasach
    - Zgodność liczby luk z liczbą odpowiedzi
    
    Args:
        content: Treść testu do sprawdzenia
        
    Returns:
        bool: True jeśli struktura jest poprawna
    """
    # Sprawdzamy czy są luki w tekście
    if not re.search(r'\[ _ \]', content):
        return False
        
    # Sprawdzamy odpowiedzi na końcu
    if not re.search(r'\[.*\]$', content):
        return False
        
    return True
```

## Struktura aplikacji i logika biznesowa

### Modele danych
Implementacja w `models.py`:

```python
class Test(models.Model):
    """
    Główny model testu.
    
    Pola:
    - title: nazwa testu
    - test_type: typ testu (wybór z predefiniowanej listy)
    - content: surowa treść przed parsowaniem
    - word_list: lista słów dla typu TEXT_INPUT_WORDLIST
    """
    title = models.CharField(max_length=200)
    # ... reszta implementacji w models.py
```

### Obsługiwane typy testów

1. TEXT_INPUT_MEMORY:
   - Cel: wypełnianie luk z pamięci
   - Brak listy słów do wyboru
   - Format luk: [ _ ]
   - Odpowiedzi na końcu w nawiasach [słowo1,słowo2]

2. TEXT_INPUT_WORDLIST:
   - Cel: wypełnianie luk z podanej listy
   - Lista słów na początku (np. "at - in - on")
   - Format luk: [ _ ]
   - Odpowiedzi muszą pochodzić z listy

[pozostałe typy...]

## System parsowania testów

### Format luk - ważne zmiany
Ujednolicony format: `[ _ ]`

Uzasadnienie zmiany:
- Jednolity format dla wszystkich typów testów
- Łatwiejsze parsowanie (jeden wzorzec regex)
- Mniejsza szansa na błędy przy tworzeniu testów
- Lepsze doświadczenie użytkownika

```python
# Prawidłowy wzorzec dla wyszukiwania luk
gap_pattern = r'\[ _ \]'

# Przykład użycia:
text = "Complete: [ _ ] sentence"
parts = re.split(gap_pattern, text)
# parts = ['Complete: ', '', ' sentence']
```

### Struktura sparsowanych danych

#### Testy z lukami:
```python
[
    [  # Pojedyncze pytanie
        {"text": "Dokończ zdanie: ", "gap": False},
        {"text": "", "gap": True, "id": 1},  # Luka
        {"text": " znajduje się tutaj.", "gap": False}
    ]
]
```

Wyjaśnienie struktury:
- Lista pytań (zewnętrzna lista)
- Każde pytanie to lista części (teksty i luki)
- Każda część ma określony typ (tekst/luka)
- Luki mają unikalne ID dla powiązania z odpowiedziami

[pozostałe struktury danych...]

## Proces testowania

### Testy jednostkowe
Implementacja w `tests.py`:

```python
def test_parse_gap_test(self):
    """
    Test parsowania testu z lukami.
    
    Sprawdzamy:
    - Czy wynikowa struktura jest listą
    - Czy pytania mają prawidłowy format
    - Czy luki są prawidłowo oznaczone
    """
    test_content = "Complete: [ _ ] sentence"
    result = parse_gap_test(test_content)
    
    self.assertIsInstance(result, list)
    # ... pozostałe asercje
```

### Proces debugowania
Dodane punkty debugowania w kodzie:

```python
# views.py
def form_valid(self, form):
    """
    Obsługa poprawnie wypełnionego formularza.
    Zapisujemy dane w sesji i przekierowujemy do podglądu.
    """
    print("=== Dane formularza ===")  # Debug
    print("Typ testu:", form.cleaned_data['test_type'])
    print("Treść:", form.cleaned_data['content'])
    # ... reszta implementacji
```

## Wdrażanie zmian

### Proces wprowadzania zmian
1. Aktualizacja CHANGELOG.md z opisem zmian
2. Wykonanie testów jednostkowych
3. Aktualizacja dokumentacji (ten plik)
4. Commit ze szczegółowym opisem
5. Push do repozytorium

### Migracje bazy danych
```bash
# Tworzenie migracji
python manage.py makemigrations

# Sprawdzenie SQL migracji (opcjonalne)
python manage.py sqlmigrate app_name migration_name

# Wykonanie migracji
python manage.py migrate
```

## Znane problemy i rozwiązania

### Problem z formatem luk
Problem: Niespójność w użyciu różnych formatów luk
Rozwiązanie: Ujednolicenie do formatu [ _ ]

[inne znane problemy i rozwiązania...]

## Przyszły rozwój
Szczegółowe plany znajdują się w TODO.md. Główne kierunki:
- Automatyczna detekcja typu testu
- System tagów do kategoryzacji
- Panel administracyjny
- API dla integracji zewnętrznych