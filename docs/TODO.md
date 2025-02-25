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

## Przechowywanie testów i odpowiedzi

### Rozbudowa modelu danych
- [ ] Rozszerzyć model `Test` o pole przechowujące poprawne odpowiedzi
  ```python
  class Test(models.Model):
      # istniejące pola...
      correct_answers = models.JSONField(
          null=True,
          blank=True,
          help_text="Prawidłowe odpowiedzi w formacie JSON"
      )
  ```
- [ ] Dodać model `TestAttempt` do przechowywania prób rozwiązania testu
  ```python
  class TestAttempt(models.Model):
      test = models.ForeignKey(Test, on_delete=models.CASCADE)
      user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
      completed_at = models.DateTimeField(auto_now_add=True)
      user_answers = models.JSONField()
      score = models.FloatField()
      max_score = models.IntegerField()
      
      @property
      def percentage_score(self):
          return (self.score / self.max_score * 100) if self.max_score > 0 else 0
  ```
- [ ] Zmodyfikować system sesji, aby płynnie przeszedł na korzystanie z modeli bazodanowych
  ```python
  # przykład w views.py
  def save_test(request):
      # Pobierz dane z sesji
      test_data = request.session.get('test_data')
      
      # Utwórz nowy test
      test = Test(
          title=test_data['title'],
          test_type=test_data['type'],
          content=test_data['content'],
          word_list=' - '.join(test_data['word_list']) if test_data.get('word_list') else '',
          correct_answers=json.dumps(test_data['answers'])
      )
      test.save()
      
      # Opcjonalnie: przypisz do użytkownika
      if request.user.is_authenticated:
          test.created_by = request.user
          test.save()
          
      return redirect('test_detail', pk=test.pk)
  ```

### Walidatory dla różnych typów testów
- [ ] Stworzyć dedykowane klasy walidatorów dla każdego typu testu
  ```python
  # validators.py
  class TestValidator:
      """Bazowa klasa walidatora dla testów"""
      
      def validate(self, content):
          """Implementacja w klasach potomnych"""
          raise NotImplementedError
  
  class SingleChoiceValidator(TestValidator):
      """Walidator dla testów jednokrotnego wyboru"""
      
      def validate(self, content):
          # implementacja walidacji
          pass
  
  class MultipleChoiceValidator(TestValidator):
      """Walidator dla testów wielokrotnego wyboru"""
      
      def validate(self, content):
          # implementacja walidacji
          pass
          
  # Dodać pozostałe klasy walidatorów
  ```
- [ ] Zarejestrować walidatory w systemie
  ```python
  # validators_registry.py
  VALIDATORS = {
      'SINGLE_CHOICE': SingleChoiceValidator(),
      'MULTIPLE_CHOICE': MultipleChoiceValidator(),
      'CHOICE_WITH_GAPS': ChoiceWithGapsValidator(),
      'TEXT_INPUT_MEMORY': TextInputMemoryValidator(),
      'TEXT_INPUT_WORDLIST': TextInputWordlistValidator(),
  }
  
  def get_validator(test_type):
      """Zwraca odpowiedni walidator dla typu testu"""
      return VALIDATORS.get(test_type)
  ```
- [ ] Zintegrować walidatory z formularzami
  ```python
  # forms.py
  def clean(self):
      cleaned_data = super().clean()
      test_type = cleaned_data.get('test_type')
      content = cleaned_data.get('content')
      
      validator = get_validator(test_type)
      if validator:
          try:
              validator.validate(content)
          except ValidationError as e:
              raise ValidationError(str(e))
      
      return cleaned_data
  ```

## System zarządzania testami

### Zarządzanie testami
- [ ] Dodać CRUD dla testów (Create, Read, Update, Delete)
- [ ] Implementacja widoku listy testów
- [ ] Implementacja szczegółów testu
- [ ] Dodać możliwość edycji istniejących testów
- [ ] Implementacja systemu wyszukiwania i filtrowania testów

### System użytkowników i uprawnień
- [ ] Dodać uwierzytelnianie użytkowników
- [ ] Implementacja rejestracji i logowania
- [ ] Zdefiniować role (administrator, nauczyciel, uczeń)
- [ ] Zarządzanie uprawnieniami do testów

### Statystyki i analiza
- [ ] Implementacja systemu zbierania statystyk z testów
- [ ] Wizualizacja postępów ucznia
- [ ] Analiza trudności pytań
- [ ] Raportowanie wyników

## Optymalizacje UX/UI

### Doświadczenie użytkownika
- [ ] Poprawić interfejs rozwiązywania testów
- [ ] Dodać komunikaty podsumowujące wyniki
- [ ] Implementacja podpowiedzi i wyjaśnień do odpowiedzi
- [ ] Obsługa czasu na rozwiązanie testu

### Zaawansowane parsowanie
- [ ] Dodać system automatycznego wykrywania typu testu
- [ ] Obsługa różnych formatów wejściowych (markdown, txt, doc)
- [ ] Implementacja konwerterów między formatami
- [ ] Dodać obsługę importu/eksportu w różnych formatach

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