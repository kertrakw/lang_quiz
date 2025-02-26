from django import forms
import re
from django.core.exceptions import ValidationError
import logging


logger = logging.getLogger('quiz_builder.views')


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
            'placeholder': 'Enter words separated by hyphen (e.g.: at - in - on)'
        }),
        label='Word list (only for "Fill in the gaps from wordlist" type)',
        help_text='Separate words with space hyphen space'
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

        # Rozdzielamy odpowiedzi dla poszczególnych pytań
        raw_answers = answer_match.group(1).strip()
        answer_groups = [ans.strip() for ans in raw_answers.split(',')]

        # Walidacja w zależności od typu testu
        if test_type in ['SINGLE_CHOICE', 'CHOICE_WITH_GAPS']:
            # Sprawdzamy odpowiedzi dla każdego pytania
            for i, ans_group in enumerate(answer_groups):
                # Sprawdzamy czy jest dokładnie jedna odpowiedź
                if ' ' in ans_group:
                    raise ValidationError(
                        f"For question {i+1}: This type of test must have exactly one answer. "
                        f"Found multiple answers: {ans_group}"
                    )
                # Sprawdzamy czy odpowiedzi to pojedyncze litery A-D lub cyfry 1-4
                if not re.match(r'^[A-Da-d1-4]$', ans_group):
                    raise ValidationError(
                        f"For question {i+1}: Invalid answer format: {ans_group}. "
                        "For single choice tests use A-D or 1-4"
                    )

        elif test_type == 'MULTIPLE_CHOICE':
            # Sprawdzamy odpowiedzi dla każdego pytania
            for i, ans_group in enumerate(answer_groups):
                # Dzielimy odpowiedzi dla tego pytania według spacji
                answers = ans_group.split()

                # Sprawdzamy czy odpowiedzi to pojedyncze litery A-D lub cyfry 1-4
                # oraz czy nie ma duplikatów
                seen = set()
                logger.debug(f"Checking for duplicates in answers for question {i+1}: {answers}")

                for ans in answers:
                    if not re.match(r'^[A-Da-d1-4]$', ans):
                        logger.error(f"Invalid format for answer: {ans}")
                        raise ValidationError(
                            f"For question {i+1}: Invalid answer format: {ans}. "
                            "For multiple choice tests use A-D or 1-4"
                        )

                    if ans.upper() in seen:
                        logger.error(f"Duplicate answer found: {ans}")
                        logger.debug(f"Current seen answers: {seen}")
                        raise ValidationError(
                            f"For question {i+1}: Answer '{ans}' has already been used. "
                            "Each answer in multiple choice test can be used only once."
                        )
                    seen.add(ans.upper())
                    logger.debug(f"Added to seen: {ans.upper()}, current seen: {seen}")

        return answer_groups

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
            answer_groups = self.validate_answers(content, test_type)
            cleaned_data['answers'] = answer_groups

            # Walidacja dla testu z listą słów
            if test_type == 'TEXT_INPUT_WORDLIST':
                if not word_list:
                    raise ValidationError(
                        "Word list is required for 'Fill in the gaps from wordlist' type"
                    )
                # Sprawdzamy czy wszystkie słowa z word_list są użyte w odpowiedziach
                words = {w.strip() for w in word_list.split(' - ')}

                # Spłaszczamy odpowiedzi do jednej listy
                all_answers = []
                for ans_group in answer_groups:
                    if ' ' in ans_group:  # jeśli mamy format z odpowiedziami oddzielonymi spacjami
                        all_answers.extend(ans_group.split())
                    else:
                        all_answers.append(ans_group)

                unused_words = words - {ans.strip() for ans in all_answers}
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
                for ans_group in answer_groups:
                    if test_type == 'MULTIPLE_CHOICE':
                        # Dzielimy odpowiedzi według spacji dla MULTIPLE_CHOICE
                        answers = ans_group.split()
                        for ans in answers:
                            if ans.upper() not in available_options:
                                raise ValidationError(
                                    f"Answer {ans} refers to a non-existent option"
                                )
                    else:
                        # Pojedyncza odpowiedź dla innych typów
                        if ans_group.upper() not in available_options:
                            raise ValidationError(
                                f"Answer {ans_group} refers to a non-existent option"
                            )

        except ValidationError as e:
            logger.error("Validation error: %s", str(e))
            raise ValidationError(str(e))

        return cleaned_data
