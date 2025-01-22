# views.py
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic import FormView
from .forms import TestInputForm
import re

from .parsers import detect_test_type, parse_gap_test, parse_choice_test

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
        if test_type in ['TEXT_INPUT']:
            parsed_content = parse_gap_test(content)
        elif test_type in ['MULTIPLE_CHOICE', 'CHOICE_WITH_GAPS']:
            parsed_content = parse_choice_test(content)

        # Przygotowujemy dane do wyświetlenia
        context = super().get_context_data(**kwargs)
        context.update({
            'title': test_data['title'],
            'type': test_type,
            'parsed_content': parsed_content
        })

        return context

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

        # Zapisujemy dane w sesji
        self.request.session['test_data'] = {
            'title': title,
            'type': test_type,
            'content': content,
            'word_list': available_words,
            'number_of_gaps': number_of_gaps
        }
        
        return super().form_valid(form)
