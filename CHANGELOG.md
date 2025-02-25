# Changelog
Wszystkie istotne zmiany w projekcie będą dokumentowane w tym pliku.

## Wersjonowanie
Projekt stosuje [Wersjonowanie semantyczne](https://semver.org/):
- Wersja GŁÓWNA (X.0.0) - niekompatybilne zmiany API
- Wersja POMNIEJSZA (0.X.0) - dodanie funkcjonalności z zachowaniem kompatybilności wstecznej
- Wersja ŁATKA (0.0.X) - poprawki błędów z zachowaniem kompatybilności wstecznej

## Harmonogram wydań
- Wydania ŁATEK - w miarę potrzeb dla poprawek błędów
- Wydania POMNIEJSZE - co 2-3 tygodnie z nowymi funkcjami
- Wydania GŁÓWNE - nieplanowane do wersji 1.0.0

## [0.1.0] - 2025-01-22
### Dodano
- Podstawowe typy testów (TEXT_INPUT_MEMORY, TEXT_INPUT_WORDLIST)
- Parser testów dla różnych formatów
- Formularz tworzenia testów
- Funkcjonalność podglądu testów

### Zmieniono
- Zaktualizowano logikę wykrywania typu testu
- Ulepszono walidację formularza

### Naprawiono
- Obsługę testów wielolinijkowych w parserze
- Problemy z wyświetlaniem pola listy słów w formularzu

## [Nierozpocząte]
### Planowane
- Funkcjonalność zapisywania testów
- System tagów
- Uwierzytelnianie użytkowników
- Endpointy API

## [0.2.0] - 2025-01-24
### Dodano
- Obsługa różnych formatów oznaczeń odpowiedzi (a), A., 1), -)
- Automatyczna konwersja formatów na standardowy (A., B., C., D.)

### Zmieniono
- Poprawiono obsługę testu typu MULTIPLE_CHOICE
- Zmieniono sposób wykrywania typu testu w preview (użycie typu z sesji)

### Naprawiono
- Naprawiono wyświetlanie właściwych kontrolek dla MULTIPLE_CHOICE (checkboxy zamiast radio buttons)

## [0.2.1] - 2025-01-25
### Dodano
- Walidacja pojedynczej odpowiedzi dla testów jednokrotnego wyboru
- Szczegółowe komunikaty walidacji dla odpowiedzi

### Zmieniono
- Przetłumaczono wszystkie komunikaty błędów na angielski
- Ulepszono wyświetlanie komunikatów błędów w interfejsie formularza

### Naprawiono
- Walidację duplikatów odpowiedzi w testach wielokrotnego wyboru
- Wyświetlanie komunikatów błędów formularza
- Walidację liczby odpowiedzi dla różnych typów testów

## [0.2.2] - 2025-01-26
### Dodano
- Funkcjonalność czyszczenia numeracji pytań
- Walidacja pojedynczej odpowiedzi dla testów jednokrotnego wyboru

### Zmieniono
- Przetłumaczono wszystkie komunikaty błędów na angielski
- Ulepszono wyświetlanie komunikatów błędów w interfejsie formularza

### Naprawiono
- Walidację duplikatów odpowiedzi w testach wielokrotnego wyboru
- Wyświetlanie komunikatów błędów formularza
- Walidację liczby odpowiedzi dla różnych typów testów

## [0.2.3]
### Zmieniono
- Zmodyfikowano wyświetlanie testu CHOICE_WITH_GAPS
  - Zamieniono select na radio buttons dla opcji odpowiedzi
  - Dodano placeholder (_______) w miejscu luki
  - Zaimplementowano wyświetlanie wybranej odpowiedzi w luce
  - Zaktualizowano JavaScript do obsługi wyboru radio button

### Zmieniono
- Zaktualizowano przypadki testowe do aktualnych implementacji typów testów
- Dodano kompleksowe pokrycie testami dla wszystkich formatów testów
- Rozszerzono testy parsera o szczegółową walidację struktury

### Dodano
- Dokumentację schematu wersjonowania
- Informacje o harmonogramie wydań

## [0.2.4] - 2025-02-18
### Zmieniono
- Zmieniono framework CSS z Bootstrap 5 na Bulma 0.9.4
- Zaktualizowano wszystkie szablony aby korzystały z klas Bulma
- Usunięto zależność od Bootstrap JS

## [0.2.5] - 2025-02-19
### Zmieniono
- Zmieniono sposób dostarczania Bulmy z CDN na npm
- Dodano kompilację SCSS przez Dart Sass
- Skonfigurowano strukturę plików SCSS

## [0.2.6] - 2025-02-23

### Zmieniono
- Ujednolicono format luk w testach do [ _ ]
- Poprawiono parsowanie testów z lukami
- Zaktualizowano przykładowe testy do nowego formatu

### Usunięto
- Usunięto funkcję detect_test_type (przeniesiona do planów rozwojowych)

### Naprawiono
- Poprawiono logikę w parse_gap_test dla właściwego wykrywania luk
- Naprawiono numerację luk w sparsowanych testach

### Dokumentacja
- Dodano docs/TODO.md z planami rozwojowymi
- Zaktualizowano dokumentację formatów testów
- Dodano szczegółowe przykłady użycia nowego formatu luk

## [0.2.7] - [2025-02-24]

### Zmieniono
- Zmieniono separator słów na liście (w testach typu TEXT_INPUT_WORDLIST) z ',' na ' - '
- Zastąpiono element datalist elementem select w testach typu TEXT_INPUT_WORDLIST
- Poprawiono interfejs wyboru słów dla bardziej intuicyjnego doświadczenia użytkownika
- Rozwiązano problem z filtrowaniem opcji po wyborze w listach rozwijanych
- Dostosowano obsługę komunikatów błędów dla zwiększenia przejrzystości logów
- Ujednolicono format komunikatów diagnostycznych

### Dodano
- Zaimplementowano system logowania dla lepszego debugowania aplikacji
- Dodano konfigurację logowania w settings.py z zapisem do pliku i konsoli
- Zastąpiono instrukcje print wywołaniami loggera o odpowiednich poziomach


## [0.2.8] - [2025-02-25]

### Naprawiono
- Problem wrażliwości na wielkość liter w testach z listą słów
- Ustandaryzowano obsługę słów dla spójnej walidacji niezależnie od wielkości liter
- Zaimplementowano konwersję do małych liter przy porównywaniu słów w szablonach i widokach
- Naprawiono błąd wyświetlania testów typu TEXT_INPUT_MEMORY, które nieprawidłowo pokazywały pustą listę słów i pola select zamiast pól input
- Dodano sprawdzanie typu testu w szablonie _gap_test.html, aby zapewnić właściwe renderowanie różnych typów testów
- Poprawiono układ interfejsu testów wyboru
- Numer pytania i treść pytania są teraz wyświetlane w jednej linii
- Opcje odpowiedzi są wyświetlane obok przycisków radio/checkbox zamiast pod nimi
- Naprawiono brakujące narzędzia flexbox z Bulma, dodając helper visibility
- Zwiększono czytelność testów typu wyboru
- Naprawiono problem z wykrywaniem luk w testach typu CHOICE_WITH_GAPS
- Zmodyfikowano regex do dzielenia tekstu, aby zachować informację o lukach
- Poprawiono renderowanie placeholderów luk w szablonie
- Naprawiono parsowanie i walidację odpowiedzi w testach typu MULTIPLE_CHOICE
- Zaktualizowano system sprawdzania odpowiedzi dla testów wielokrotnego wyboru
- Poprawiono obsługę formularzy z wielokrotnym wyborem (checkboxy)
- Zapewniono spójną obsługę wielkości liter w odpowiedziach
- Naprawiono obsługę testów wielokrotnego wyboru (MULTIPLE_CHOICE) w systemie sprawdzania
- Dodano wsparcie dla wielu zaznaczonych wartości (checkboxy) w widoku sprawdzania
- Poprawiono porównywanie odpowiedzi w testach wielokrotnego wyboru
- Ulepszono normalizację formatu odpowiedzi (wielkość liter, białe znaki)

### Dodano
- Przycisk "Example Test" obok przycisku tworzenia testu
- Modal z przykładami dla wszystkich typów testów
- Dynamiczne wyświetlanie przykładu w zależności od wybranego typu testu
- Style CSS zapewniające poprawne zawijanie tekstu w przykładach

## [0.2.9] - [2025-02-26]

### Dodano
- Przycisk "Example Test" obok przycisku tworzenia testu
- Modal z przykładami dla wszystkich typów testów
- Dynamiczne wyświetlanie przykładu w zależności od wybranego typu testu
- Style CSS zapewniające poprawne zawijanie tekstu w przykładach
- Stronę wyników testu pokazującą ocenę i szczegółowe informacje
- Możliwość próby ponownego rozwiązania testu lub edycji
- Pakiet templatetags z niestandardowymi filtrami dla szablonów

### Zmieniono
- Zaktualizowano TestCheckView aby przekierowywał na stronę wyników
- Ulepszono prezentację wyników testu z kolorowym oznaczeniem poprawnych/niepoprawnych odpowiedzi



