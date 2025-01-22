from django.db import models

class Test(models.Model):
    # Podstawowe informacje o teście
    title = models.CharField(max_length=200)  # Tytuł testu
    
    # Typ testu - wybierany z predefiniowanych opcji
    test_type = models.CharField(
        max_length=20, 
        choices=[
            ('TEXT_INPUT_MEMORY', 'Fill in the gaps from memory'),  # Test z lukami - wpisywanie z pamięci
            ('CHOICE_QUESTIONS', 'Multiple choice questions'),      # Test wyboru (obejmuje zarówno wybór z listy jak i pojedyncze wybory)
            ('MULTIPLE_CHOICE', 'Multiple correct answers')         # Test z wieloma poprawnymi odpowiedziami
        ]
    )
    
    # Dodajemy pole określające sposób wyświetlania dla typu CHOICE_QUESTIONS
    display_type = models.CharField(
        max_length=20,
        choices=[
            ('DROPDOWN', 'Single dropdown with all options'),  # Jedna lista rozwijana dla wszystkich luk
            ('RADIO', 'Individual radio buttons'),            # Osobne przyciski radio dla każdego pytania
        ],
        null=True,  # Pole może być puste dla innych typów testów
        blank=True
    )
    
    # Surowa treść testu - przed sparsowaniem
    content = models.TextField()
    
    # Data utworzenia testu - automatycznie ustawiana przy tworzeniu
    created_at = models.DateTimeField(auto_now_add=True)

    word_list = models.TextField(
        null=True, 
        blank=True, 
        help_text="Available words for TEXT_INPUT_WORDLIST type. Separate words with commas."
    )  # Lista słów do wyboru dla typu TEXT_INPUT_WORDLIST

    def __str__(self):
        # Metoda określająca jak obiekt będzie wyświetlany w panelu admina i konsoli
        return f"{self.title} ({self.test_type})"
    
    def get_word_list(self):
        """
        Metoda pomocnicza zwracająca listę słów jako listę pythonową
        """
        if self.word_list:
            return [word.strip() for word in self.word_list.split(',')]
        return []


class Question(models.Model):
    # Relacja z modelem Test - każde pytanie jest przypisane do konkretnego testu
    # on_delete=models.CASCADE oznacza, że pytanie zostanie usunięte gdy test zostanie usunięty
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    
    # Treść pytania
    question_text = models.TextField()
    
    # Poprawna odpowiedź - używana dla testów TEXT_INPUT i WORD_CHOICE
    correct_answer = models.TextField()
    
    # Lista dostępnych słów do wyboru - tylko dla testu typu WORD_CHOICE
    # null=True i blank=True pozwalają na pozostawienie tego pola pustym dla innych typów testów
    available_words = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Question for {self.test.title}: {self.question_text[:50]}..."


class Choice(models.Model):
    # Relacja z modelem Question - każdy wybór jest przypisany do konkretnego pytania
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    # Treść wyboru/odpowiedzi
    choice_text = models.CharField(max_length=200)
    
    # Określa czy ten wybór jest poprawną odpowiedzią
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Choice for {self.question.test.title}: {self.choice_text}"
