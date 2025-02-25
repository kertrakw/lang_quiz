# views.py
from django.shortcuts import redirect  # type: ignore
from django.views.generic import TemplateView  # type: ignore
from django.views.generic import FormView  # type: ignore
from django.views import View  # type: ignore
from django.http import JsonResponse
# from django.core.exceptions import ValidationError
from .forms import TestInputForm
# import re
import logging

from .parsers import parse_gap_test, parse_choice_test


logger = logging.getLogger('quiz_builder.views')

# Widok strony głównej - wyświetla podstawowy interfejs do tworzenia testów
class HomeView(TemplateView):
    template_name = 'tests/home.html'


class TestPreviewView(TemplateView):
    template_name = 'tests/preview_test.html'

    def get_context_data(self, **kwargs):
        # Pobieramy dane z sesji
        test_data = self.request.session.get('test_data')

        if not test_data:
            return redirect('create_test')

        content = test_data['content']
        test_type = test_data['type']  # bierzemy typ z sesji

        # Parsujemy w zależności od wykrytego typu
        logger.debug("===== Test type from session: %s", test_type)
        if test_type in ['TEXT_INPUT_MEMORY', 'TEXT_INPUT_WORDLIST']:
            parsed_content = parse_gap_test(content)
        elif test_type in ['SINGLE_CHOICE', 'MULTIPLE_CHOICE', 'CHOICE_WITH_GAPS']:
            parsed_content = parse_choice_test(content, test_type)

        logger.debug("Parsed content: %s", parsed_content)

        context = super().get_context_data(**kwargs)
        context.update({
            'title': test_data['title'],
            'type': test_type,  # używamy typu z sesji
            'parsed_content': parsed_content,
            'word_list': test_data.get('word_list', [])  # Dodajemy word_list do kontekstu
        })
        logger.debug("Context: %s", context)
        return context


class TestCheckView(View):
    def post(self, request):
        # Pobieramy dane testu z sesji
        test_data = request.session.get('test_data')
        if not test_data:
            return JsonResponse({'error': 'No test data found'}, status=400)

        # Pobieramy przesłane odpowiedzi
        answers = {}
        for key, value in request.POST.items():
            if key.startswith('answer_'):
                # Dla MULTIPLE_CHOICE pobieramy wszystkie zaznaczone wartości
                if test_data['type'] == 'MULTIPLE_CHOICE':
                    values = request.POST.getlist(key)
                    answers[key] = values
                else:
                    answers[key] = value

        # Sprawdzamy odpowiedzi
        results = self.check_answers(test_data, answers)

        return JsonResponse(results)

    def check_answers(self, test_data, submitted_answers):
        """
        Sprawdza poprawność odpowiedzi.
        Zwraca słownik z wynikami dla każdej odpowiedzi.
        """
        test_type = test_data.get('type', '')
        correct_answers = test_data.get('answers', {})
        
        results = {
            'total': len(correct_answers),
            'correct': 0,
            'answers': {}
        }

        # Sprawdzamy każdą odpowiedź
        for q_id, correct in correct_answers.items():
            answer_key = f'answer_{q_id}'
            submitted = submitted_answers.get(answer_key, '')
            
            # Obsługa różnych typów testów
            if test_type == 'MULTIPLE_CHOICE':
                # Konwertuj prawidłowe odpowiedzi na listę, jeśli są oddzielone spacjami
                correct_list = correct.split() if isinstance(correct, str) else correct
                correct_list = [ans.upper() for ans in correct_list]
                
                # Pobierz odpowiedzi użytkownika jako listę
                submitted_list = submitted if isinstance(submitted, list) else [submitted]
                submitted_list = [ans.upper() for ans in submitted_list if ans.strip()]
                
                # Sprawdź czy zbiory odpowiedzi są identyczne
                is_correct = set(submitted_list) == set(correct_list)
                
                results['answers'][q_id] = {
                    'submitted': submitted_list,
                    'correct': correct_list,
                    'is_correct': is_correct
                }
            else:
                # Konwertujemy do jednolitego formatu (wielkie litery, usunięcie spacji)
                correct_norm = correct.upper().strip() if isinstance(correct, str) else ''
                submitted_norm = submitted.upper().strip() if isinstance(submitted, str) else ''
                
                is_correct = submitted_norm == correct_norm
                
                results['answers'][q_id] = {
                    'submitted': submitted,
                    'correct': correct,
                    'is_correct': is_correct
                }

            if is_correct:
                results['correct'] += 1

        results['percentage'] = (results['correct'] / results['total']) * 100 if results['total'] > 0 else 0

        return results


class TestCreateView(FormView):
    template_name = 'tests/create_test.html'  # Szablon, który utworzymy
    form_class = TestInputForm
    success_url = '/test/preview/'  # URL, na który przekierujemy po udanym przesłaniu formularza

    # views.py - w klasie TestCreateView, metoda form_valid
    def form_valid(self, form):
        """
        Metoda wywoływana gdy formularz jest poprawnie wypełniony.
        Walidacja jest już wykonana w formularzu.
        """
        # Pobieramy wyczyszczone dane
        cleaned_data = form.cleaned_data
        content = cleaned_data['content']
        test_type = cleaned_data['test_type']
        answers = cleaned_data.get('answers', [])

        logger.info("=== Form validation passed ===")
        logger.debug("Content: %s", content)
        logger.debug("Type: %s", test_type)
        logger.debug("Answers: %s", answers)

        # Konwertujemy odpowiedzi na słownik dla TestCheckView
        answers_dict = {str(i+1): ans for i, ans in enumerate(answers)}
        logger.debug("Answers dict: %s", answers_dict)

        # Przygotowujemy dane do sesji
        self.request.session['test_data'] = {
            'title': cleaned_data['title'],
            'type': test_type,
            'content': content,
            'word_list': [word.strip().lower() for word in cleaned_data.get('word_list', '').split(' - ')],
            'answers': {k: v.lower() for k, v in answers_dict.items()}
        }

        return super().form_valid(form)

    def form_invalid(self, form):
        logger.error("Form errors: %s", form.errors)
        return super().form_invalid(form)
