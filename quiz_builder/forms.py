from django import forms
import re
from django.core.exceptions import ValidationError


# Formularz do tworzenia nowego testu - obsługuje różne typy testów i walidację danych
class TestInputForm(forms.Form):
    # Pole na tytuł testu
    title = forms.CharField(
        max_length=200,
        label='Test title',  # Etykieta wyświetlana w formularzu
        widget=forms.TextInput(attrs={'class': 'input'})
        # Zmieniamy form-control na input dla Bulma
    )

    # Pole wyboru typu testu
    test_type = forms.ChoiceField(
        choices=[
            ('TEXT_INPUT_MEMORY', 'Fill in the gaps from memory'),
            ('TEXT_INPUT_WORDLIST', 'Fill in the gaps from wordlist'),
            ('SINGLE_CHOICE', 'Single choice test'),
            ('MULTIPLE_CHOICE', 'Multiple choice test'),
            ('CHOICE_WITH_GAPS', 'Choice test with gaps')
        ],
        label='Test type',
        widget=forms.Select(attrs={'class': 'select'})
    )

    word_list = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea',
            'rows': 3,
            'placeholder': 'Enter words separated by commas (e.g.: at, in, on)'
        }),
        label='Word list (only for "Fill in the gaps from wordlist" type)',
        help_text='Separate words with commas'
    )

    # Pole na treść testu
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'textarea',
            'rows': 10,  # Wysokość pola tekstowego
            'placeholder': 'Paste your test content here...'  # Tekst podpowiedzi
        }),
        label='Test content'
    )

    def validate_answers(self, content, test_type):
        """
        Sprawdza poprawność odpowiedzi w nawiasach kwadratowych.

        Args:
            content (str): Treść testu
            test_type (str): Typ testu

        Returns:
            list: Lista poprawnych odpowiedzi lub None jeśli nie znaleziono

        Raises:
            ValidationError: Gdy format odpowiedzi jest niepoprawny
        """
        # Szukamy odpowiedzi w nawiasach kwadratowych na końcu tekstu
        answer_match = re.search(r'\[(.*?)\]$', content.strip())
        if not answer_match:
            raise ValidationError("No answers found in square brackets at the end of the test")

        answers = [ans.strip() for ans in answer_match.group(1).split(',')]

        # Walidacja w zależności od typu testu
        if test_type in ['SINGLE_CHOICE', 'CHOICE_WITH_GAPS']:

            # Sprawdzamy czy jest dokładnie jedna odpowiedź
            if len(answers) > 1:
                raise ValidationError(
                    "This type of test must have exactly one answer. "
                    f"Found {len(answers)} answers: [{', '.join(answers)}]"
                )
            # Sprawdzamy czy odpowiedzi to pojedyncze litery A-D lub cyfry 1-4
            for ans in answers:
                if not re.match(r'^[A-Da-d1-4]$', ans):
                    raise ValidationError(
                        f"Invalid answer format: {ans}. "
                        "For single choice tests use A-D or 1-4"
                    )
        elif test_type == 'MULTIPLE_CHOICE':
            # Sprawdzamy czy odpowiedzi to pojedyncze litery A-D lub cyfry 1-4
            # oraz czy nie ma duplikatów
            seen = set()
            print(f"Checking for duplicates in answers: {answers}")  # Debug
            for ans in answers:

                if not re.match(r'^[A-Da-d1-4]$', ans):
                    print(f"Invalid format for answer: {ans}")  # Debug
                    raise ValidationError(
                        f"Invalid answer format: {ans}. "
                        "For multiple choice tests use A-D or 1-4"
                    )
                if ans.upper() in seen:
                    print(f"Duplicate answer found: {ans}")  # Debug
                    print(f"Current seen answers: {seen}")  # Debug
                    raise ValidationError(
                        f"Answer '{ans}' has already been used. "
                        "Each answer in multiple choice test can be used only once."
                    )
                seen.add(ans.upper())
                print(f"Added to seen: {ans.upper()}, current seen: {seen}")
                # Debug

        return answers

    def clean(self):
        """
        Walidacja formularza z uwzględnieniem struktury testu.
        """
        cleaned_data = super().clean()
        test_type = cleaned_data.get('test_type')
        content = cleaned_data.get('content')
        word_list = cleaned_data.get('word_list')

        if not content:
            return cleaned_data

        try:
            # Jednorazowa walidacja odpowiedzi
            answers = self.validate_answers(content, test_type)
            cleaned_data['answers'] = answers

            # Walidacja dla testu z listą słów
            if test_type == 'TEXT_INPUT_WORDLIST':
                if not word_list:
                    raise ValidationError(
                        "Word list is required for 'Fill in the gaps from wordlist' type"
                    )
                # Sprawdzamy czy wszystkie słowa z word_list są użyte w odpowiedziach
                words = {w.strip() for w in word_list.split(',')}
                unused_words = words - {ans.strip() for ans in answers}
                if unused_words:
                    raise ValidationError(
                        f"Following words from the list are not used in the test: "
                        f"{', '.join(unused_words)}"
                    )

            # Walidacja dla testów wyboru
            elif test_type in ['SINGLE_CHOICE', 'MULTIPLE_CHOICE', 'CHOICE_WITH_GAPS']:
                # Sprawdzamy czy są opcje wyboru
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                options_found = False
                available_options = set()

                for line in lines:
                    match = re.match(r'^([A-Da-d1-4])[.).]\s', line)
                    if match:
                        options_found = True
                        available_options.add(match.group(1).upper())

                if not options_found:
                    raise ValidationError(
                        "Choice test must contain options marked "
                        "as A., B., C., D. or 1., 2., 3., 4."
                    )

                # Sprawdzamy czy odpowiedzi odnoszą się do istniejących opcji
                for ans in answers:
                    if ans.upper() not in available_options:
                        raise ValidationError(
                            f"Answer {ans} refers to a non-existent option"
                        )

        except ValidationError as e:
            print(f"Validation error: {str(e)}")  # debug
            raise ValidationError(str(e))

        return cleaned_data