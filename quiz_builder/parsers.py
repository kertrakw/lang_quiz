import re


def standardize_choice_marker(text):
    """
    Konwertuje różne formaty oznaczeń na standardowy format A., B., C., D.

    Akceptuje formaty:
    - A., A), a., a), (A), (a)
    - 1., 1), (1)
    - myślnik (-)

    Args:
       text (str): Tekst zaczynający się od oznaczenia (np. "A) odpowiedź" lub "- odpowiedź")

    Returns:
       tuple: (standardowy_marker, treść_odpowiedzi) np. ("A", "odpowiedź")
    """
    # Usuwamy whitespace z początku
    text = text.strip()

    # Jeśli zaczyna się od myślnika
    if text.startswith('-'):
        return None, text[1:].strip()

    # Szukamy różnych formatów na początku tekstu
    marker_match = re.match(r'^[(\s]*([A-Da-d]|[1-4])[.).]\s*(.+)$', text)

    if marker_match:
        marker, content = marker_match.groups()

        # Konwertujemy cyfry na litery (1->A, 2->B, itd.)
        if marker.isdigit():
            marker = chr(ord('A') + int(marker) - 1)

        # Konwertujemy na wielką literę
        marker = marker.upper()

        return marker, content.strip()

    return None, text


def clean_question_text(text):
    """
    Usuwa numerację z początku pytania.

    Args:
        text (str): Tekst pytania

    Returns:
        str: Tekst bez numeracji
    """
    return re.sub(r'^\s*\d+[\s.).]+', '', text.strip())


def parse_gap_test(content):
    """
    Parsuje test z lukami (zarówno jednolinijkowy jak i wielolinijkowy)
    """
    # Najpierw usuwamy linię z odpowiedziami
    content = re.sub(r'\[.*?\]$', '', content).strip()

    # Dzielimy na linijki
    lines = content.split('\n')
    questions = []

    for line in lines:
        if not line.strip():  # Pomijamy puste linie
            continue

        # Usuwamy numerację z początku linii
        line = clean_question_text(line)

        # Znajdujemy wszystkie luki w linii
        parts = re.split(r'\[ _ \]', line)

        current_question = []
        for i, part in enumerate(parts):
            if i == len(parts) - 1:  # ostatnia część
                current_question.append({
                    "text": part,
                    "gap": False
                })
            else:  # po każdej części (oprócz ostatniej) powinna być luka
                current_question.append({
                    "text": part,
                    "gap": False
                })
                current_question.append({
                    "text": "",
                    "gap": True,
                    "id": len(questions) + 1
                })

        questions.append(current_question)

    return questions


def parse_choice_test(content, test_type):
    """
    Parsuje test wyboru (SINGLE_CHOICE, MULTIPLE_CHOICE, CHOICE_WITH_GAPS)

    Args:
        content (str): Treść testu
        test_type (str): Typ testu ('SINGLE_CHOICE', 'MULTIPLE_CHOICE', 'CHOICE_WITH_GAPS')

    Returns:
        list: Lista pytań z odpowiedziami
    """
    # Znajdujemy odpowiedzi w nawiasach kwadratowych na końcu
    answer_match = re.search(r'\[(.*?)\]$', content.strip())
    answers = []
    if answer_match:
        # Pobieramy odpowiedzi i dzielimy je według przecinków
        raw_answers = answer_match.group(1).strip()
        if test_type == 'MULTIPLE_CHOICE':
            # Dla MULTIPLE_CHOICE dzielimy według przecinków,
            # #a potem każdą odpowiedź dzielimy według spacji
            answers = [ans.strip().split() for ans in raw_answers.split(',')]
        else:
            # Dla pozostałych typów pozostawiamy format z przecinkami
            answers = [ans.strip() for ans in raw_answers.split(',')]

    # Usuwamy linię z odpowiedziami przed parsowaniem reszty zawartości
    content = re.sub(r'\[.*?\]$', '', content).strip()

    # Dzielimy według pustych linii lub numeracji pytań
    questions_raw = re.split(r'\n(?=\d+\.)|(\n\s*\n)', content.strip())
    questions_raw = [q for q in questions_raw if q and q.strip()]

    questions = []

    for i, q_raw in enumerate(questions_raw):
        if not q_raw.strip():  # Pomijamy puste
            continue

        # Dzielimy na pytanie i odpowiedzi
        parts = q_raw.split('\n')

        # Usuwamy numerację z początku pytania
        question_text = clean_question_text(parts[0])

        # Znajdujemy odpowiedzi
        choices = []
        choice_letter = 'A'  # do automatycznego numerowania

        for part in parts[1:]:
            part = part.strip()
            if not part:
                continue

            marker, choice_text = standardize_choice_marker(part)

            if marker is None:
                # Jeśli nie znaleziono markera, używamy automatycznego
                marker = choice_letter

            choices.append({
                "text": choice_text,
                "letter": marker.upper()  # Upewniamy się, że litera jest wielka
            })

            # Przygotowujemy następną literę dla automatycznego numerowania
            choice_letter = chr(ord(choice_letter) + 1)

        # Przygotowujemy pytanie w zależności od typu testu
        question_data = {
            "id": len(questions) + 1,
            "choices": choices,
            "multiple_answers": test_type == 'MULTIPLE_CHOICE',
            "text": question_text,  # domyślnie cały tekst
            "has_gap": False  # domyślnie bez luk
        }

        # Dodajemy informację o poprawnych odpowiedziach jeśli są dostępne
        if answers and i < len(answers):
            if test_type == 'MULTIPLE_CHOICE':
                # Konwertujemy odpowiedzi na wielkie litery dla spójności
                question_data["correct_answers"] = [ans.upper() for ans in answers[i]]
            else:
                question_data["correct_answer"] = answers[i].upper()

        # Tylko jeśli to CHOICE_WITH_GAPS, zmieniamy strukturę tekstu
        if test_type == 'CHOICE_WITH_GAPS':
            # Znajdź wszystkie luki w tekście
            gap_pattern = r'\[ _ \]'

            # Tworzymy listę części tekstu, naprzemiennie tekst i luka
            parts = []
            segments = re.split(f'({gap_pattern})', question_text)

            for segment in segments:
                is_gap = segment == '[ _ ]'
                parts.append({
                    "content": segment if not is_gap else "",
                    "is_gap": is_gap
                })

            question_data["text"] = parts
            question_data["has_gap"] = True

        questions.append(question_data)

    return questions
