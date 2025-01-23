# views.py
from django.shortcuts import render, redirect # type: ignore
from django.views.generic import TemplateView # type: ignore
from django.views.generic import FormView # type: ignore
from django.views import View # type: ignore
from django.http import JsonResponse # type: ignore
from .forms import TestInputForm
import re

from .parsers import detect_test_type, parse_gap_test, parse_choice_test

# Widok strony głównej - wyświetla podstawowy interfejs do tworzenia testów
class HomeView(TemplateView):
    template_name = 'tests/home.html'

class TestPreviewView(TemplateView):
    template_name = 'tests/preview_test.html'

    def get_context_data(self, **kwargs):
        # Pobieramy dane z sesji
        test_data = self.request.session.get('test_data')
        
        if not test_data:
            # Jeśli nie ma danych w sesji, przekierowujemy do tworzenia testu
            return redirect('create_test')
        
        content = test_data['content']
        test_type = detect_test_type(content)
        
        # Parsujemy w zależności od wykrytego typu
        if test_type in ['TEXT_INPUT_MEMORY', 'TEXT_INPUT_WORDLIST']:
            parsed_content = parse_gap_test(content)
        elif test_type in ['SINGLE_CHOICE', 'MULTIPLE_CHOICE', 'CHOICE_WITH_GAPS']:
            parsed_content = parse_choice_test(content, test_type)

        # Przygotowujemy dane do wyświetlenia
        context = super().get_context_data(**kwargs)
        context.update({
            'title': test_data['title'],
            'type': test_type,
            'parsed_content': parsed_content
        })

        return context
    
class TestCheckView(View):
    def post(self, request):
        # Pobieramy dane testu z sesji
        test_data = request.session.get('test_data')
        if not test_data:
            return JsonResponse({'error': 'No test data found'}, status=400)
        
        # Pobieramy przesłane odpowiedzi
        answers = {
            key: value for key, value in request.POST.items() 
            if key.startswith('answer_')
        }
        
        # Sprawdzamy odpowiedzi
        results = self.check_answers(test_data, answers)
        
        return JsonResponse(results)
    
    def check_answers(self, test_data, submitted_answers):
        """
        Sprawdza poprawność odpowiedzi.
        Zwraca słownik z wynikami dla każdej odpowiedzi.
        """
        correct_answers = test_data.get('answers', [])  # Tu trzeba będzie dodać odpowiedzi do test_data
        results = {
            'total': len(correct_answers),
            'correct': 0,
            'answers': {}
        }
        
        # Sprawdzamy każdą odpowiedź
        for q_id, correct in correct_answers.items():
            answer_key = f'answer_{q_id}'
            submitted = submitted_answers.get(answer_key, '').strip().lower()
            is_correct = submitted == correct.lower()
            
            results['answers'][q_id] = {
                'submitted': submitted,
                'correct': correct,
                'is_correct': is_correct
            }
            
            if is_correct:
                results['correct'] += 1
                
        results['percentage'] = (results['correct'] / results['total']) * 100
        
        return results

class TestCreateView(FormView):
    template_name = 'tests/create_test.html'  # Szablon, który utworzymy
    form_class = TestInputForm
    success_url = '/test/preview/'  # URL, na który przekierujemy po udanym przesłaniu formularza

    def form_valid(self, form):
        # Ta metoda jest wywoływana gdy formularz jest poprawnie wypełniony
        
        # Pobieramy dane z formularza
        title = form.cleaned_data['title']
        test_type = form.cleaned_data['test_type']
        content = form.cleaned_data['content']
        word_list = form.cleaned_data.get('word_list', '')
        
        # Parsujemy zawartość testu
        gaps = re.findall(r'___', content)  # Znajdujemy wszystkie luki w teście
        number_of_gaps = len(gaps)
        
        # Jeśli mamy listę słów, przetwarzamy ją
        available_words = []
        if word_list:
            available_words = [word.strip() for word in word_list.split(',')]

        # Znajdujemy odpowiedzi w nawiasach kwadratowych [at,on,at,in,on]
        answer_match = re.search(r'\[(.*?)\]', content)
        if answer_match:
            answers_str = answer_match.group(1)
            answers_list = [ans.strip() for ans in answers_str.split(',')]
            
            # Tworzymy słownik odpowiedzi
            answers = {
                str(i+1): answer for i, answer in enumerate(answers_list)
            }
            
            # Usuwamy linię z odpowiedziami z treści testu
            content = re.sub(r'\[.*?\]', '', content).strip()
        
        # Zapisujemy w sesji
        self.request.session['test_data'] = {
            'title': form.cleaned_data['title'],
            'type': form.cleaned_data['test_type'],
            'content': content,
            'word_list': form.cleaned_data.get('word_list', '').split(','),
            'answers': answers  # dodajemy odpowiedzi
        }
        
        return super().form_valid(form)
