from django import forms

# Formularz do tworzenia nowego testu - obsługuje różne typy testów i walidację danych
class TestInputForm(forms.Form):
    # Pole na tytuł testu
    title = forms.CharField(
        max_length=200,
        label='Test title',  # Etykieta wyświetlana w formularzu
        widget=forms.TextInput(attrs={'class': 'form-control'})  # Dodajemy klasę Bootstrap dla lepszego wyglądu
    )
    
    # Pole wyboru typu testu
    test_type = forms.ChoiceField(
        choices=[
            ('TEXT_INPUT_MEMORY', 'Fill in the gaps from memory'),
            ('TEXT_INPUT_WORDLIST', 'Fill in the gaps from wordlist'),
            ('SINGLE_CHOICE', 'Single choice test'),
            ('MULTIPLE_CHOICE', 'Multiple choice test')
        ],
        label='Test type',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    word_list = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter words separated by commas (e.g.: at, in, on)'
        }),
        label='Word list (only for "Fill in the gaps from wordlist" type)',
        help_text='Separate words with commas'
    )
    
    # Pole na treść testu
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10,  # Wysokość pola tekstowego
            'placeholder': 'Paste your test content here...'  # Tekst podpowiedzi
        }),
        label='Test content'
    )
    
    def clean(self):
        """
        Metoda walidująca formularz
        """
        cleaned_data = super().clean()
        test_type = cleaned_data.get('test_type')
        word_list = cleaned_data.get('word_list')

        # Jeśli typ to TEXT_INPUT_WORDLIST, lista słów jest wymagana
        if test_type == 'TEXT_INPUT_WORDLIST' and not word_list:
            raise forms.ValidationError(
                "Word list is required for 'Fill in the gaps from wordlist' type"
            )

        return cleaned_data