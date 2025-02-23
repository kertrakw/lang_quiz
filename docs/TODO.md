# TODO List

## Planowany rozwój testów

### Testy parsera
- [ ] Testy dla edge cases formatowania:
  ```python
  def test_parser_edge_cases(self):
      """
      Testuje skrajne przypadki formatowania testów
      - Nadmiarowe spacje w lukach
      - Różne formaty numeracji (1., 1), a., A.)
      - Niestandarowe formatowanie odpowiedzi [A, B] vs [A,B]
      """
      pass
  ```

### Testy walidacji formularza
- [ ] Testy walidacji dla różnych typów testów:
  ```python
  def test_form_validation(self):
      """
      Testuje walidację formularza dla różnych typów testów:
      - Poprawna liczba odpowiedzi
      - Odpowiedzi z listy słów
      - Duplikaty w MULTIPLE_CHOICE
      """
      pass
  ```

### Testy sprawdzania odpowiedzi
- [ ] Testy dla mechanizmu sprawdzania:
  ```python
  def test_answer_checking(self):
      """
      Testuje sprawdzanie odpowiedzi:
      - Poprawne odpowiedzi
      - Częściowo poprawne odpowiedzi
      - Niepoprawne odpowiedzi
      - Brakujące odpowiedzi
      """
      pass
  ```

### Testy obsługi błędów
- [ ] Testy dla przypadków błędnych:
  ```python
  def test_error_handling(self):
      """
      Testuje obsługę błędów:
      - Brakujące odpowiedzi w nawiasach
      - Nieprawidłowy format luk
      - Niezgodność liczby luk i odpowiedzi
      """
      pass
  ```

### Testy widoków
- [ ] Rozszerzenie testów widoków:
  ```python
  class ViewTests(TestCase):
      def test_test_preview(self):
          """Test podglądu testu"""
          pass
          
      def test_test_check(self):
          """Test sprawdzania odpowiedzi"""
          pass
          
      def test_form_submission(self):
          """Test przesyłania formularza"""
          pass
  ```

## Planowane funkcjonalności
- [ ] Automatyczna detekcja typu testu
  ```python
    def detect_test_type(content):
        """
        Wykrywa typ testu na podstawie jego zawartości
        """
        # Jeśli znajdziemy listę słów na początku (np. "AT - IN - ON")
        has_word_list = bool(re.match(r'^[A-Z\s,\-–]+$', content.split('\n')[0]))

        # Jeśli znajdziemy "A.", "B.", "C." - to jest test wyboru
        has_choices = bool(re.search(r'\n[A-D]\.', content))

        # Jeśli znajdziemy lukę ([ _ ]]) - to jest test z lukami
        has_gaps = bool(re.findall(r'\[ _ \]', content))

        # Jeśli znajdziemy odpowiedzi z wieloma opcjami [A,C]
        has_multiple_answers = bool(re.search(r'\[(.*?,.*?)\]', content))

        if has_word_list and has_gaps:
            return 'TEXT_INPUT_WORDLIST'
        elif has_gaps and not has_choices:
            return 'TEXT_INPUT_MEMORY'
        elif has_choices:
            if has_multiple_answers:
                return 'MULTIPLE_CHOICE'
            elif has_gaps:
                return 'CHOICE_WITH_GAPS'
            else:
                return 'SINGLE_CHOICE'

        return None
  ```
  funkcja testowa typu pliku do pliku tests.py (ParserTests)
  ```python
      def test_detect_test_type(self):
        # Test dla TEXT_INPUT_MEMORY
        gap_test = "1. [ _ ] what time does the meeting start?"
        # Test dla SINGLE_CHOICE
        choice_test = "1. Question\nA. First\nB. Second\n[A]"
        # Test dla CHOICE_WITH_GAPS
        gap_choice_test = "Complete: [ _ ] \nA. this\nB. that\n[A]"
        # Test dla MULTIPLE_CHOICE
        multiple_choice = "1. Question\nA. First\nB. Second\n[A,B]"
        # Test dla TEXT_INPUT_WORDLIST
        wordlist_test = "IN - ON - AT\n1. [ _ ]  what time?"

        self.assertEqual(detect_test_type(gap_test), 'TEXT_INPUT_MEMORY')
        self.assertEqual(detect_test_type(choice_test), 'SINGLE_CHOICE')
        self.assertEqual(detect_test_type(gap_choice_test), 'CHOICE_WITH_GAPS')
        self.assertEqual(detect_test_type(multiple_choice), 'MULTIPLE_CHOICE')
        self.assertEqual(detect_test_type(wordlist_test), 'TEXT_INPUT_WORDLIST')
    ```
- [ ] Import testów z plików tekstowych
  ```python
  def import_from_file(file_path):
      # TODO: Implementacja importu z plików
      # - Obsługa różnych formatów (.txt, .md)
      # - Automatyczna detekcja typu
      # - Walidacja struktury
      pass
  ```
- [ ] System tagowania testów
  ```python
  # models.py
  class Tag(models.Model):
      name = models.CharField(max_length=50, unique=True)
      slug = models.SlugField(unique=True)
      
  class Test(models.Model):
      # istniejące pola...
      tags = models.ManyToManyField(Tag, blank=True)
  ```

## Bugi do naprawienia
- [ ] Problem z walidacją wielokrotnych odpowiedzi
  - Obecny kod nie wykrywa poprawnie duplikatów w formacie "A,A,B"
  - Potrzebna modyfikacja regex w `validate_answers`

## Pomysły do rozważenia

### Interfejs użytkownika
- [ ] Dodanie przykładów dla każdego typu testu
- [ ] Podgląd testu przed zapisaniem
- [ ] Tryb edycji dla istniejących testów
- [ ] System podpowiedzi przy tworzeniu testu

### Backend
- [ ] System kategorii dla testów
  ```python
  class Category(models.Model):
      name = models.CharField(max_length=100)
      parent = models.ForeignKey('self', null=True, blank=True)
      
  class Test(models.Model):
      # istniejące pola...
      category = models.ForeignKey(Category, null=True)
  ```
- [ ] API dla zewnętrznych integracji
- [ ] System eksportu testów do PDF
- [ ] Statystyki wykorzystania testów

### Logowanie i bezpieczeństwo
- [ ] System użytkowników i uprawnień
- [ ] Historia modyfikacji testów
- [ ] Zabezpieczenie przed nieautoryzowanym dostępem

## Optymalizacje wydajności
- [ ] Cache'owanie wyników parsowania
- [ ] Optymalizacja zapytań do bazy danych
- [ ] Indeksowanie często wyszukiwanych pól

## Do przedyskutowania z zespołem
- [ ] Zmiana formatu przechowywania odpowiedzi
- [ ] Rozszerzenie typów testów
- [ ] Integracja z systemami LMS

## Przypisy i dokumentacja
- [ ] Uzupełnienie docstringów
- [ ] Dokumentacja API
- [ ] Instrukcja dla użytkowników
- [ ] Przykłady użycia dla każdego typu testu