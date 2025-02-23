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
    # Usuwamy linię z odpowiedziami przed parsowaniem
    content = re.sub(r'\[.*?\]$', '', content).strip()

    # Dzielimy na pytania (według pustych linii)
    questions_raw = re.split(r'\n\s*\n', content.strip())
    questions = []

    for q_raw in questions_raw:
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
                "letter": marker
            })

            # Przygotowujemy następną literę dla automatycznego numerowania
            choice_letter = chr(ord(choice_letter) + 1)

        # Przygotowujemy pytanie w zależności od typu testu
        question_data = {
            "id": len(questions) + 1,
            "choices": choices,
            "multiple_answers": test_type == 'MULTIPLE_CHOICE',
            # to musi być PRZED przetwarzaniem tekstu
            "text": question_text,  # domyślnie cały tekst
            "has_gap": False  # domyślnie bez luk
        }

        # Tylko jeśli to CHOICE_WITH_GAPS, zmieniamy strukturę tekstu
        if test_type == 'CHOICE_WITH_GAPS':
            # Najpierw usuńmy numerację z pytania
            question_text = clean_question_text(question_text)
            # Teraz przetwarzamy tekst na części
            parts = re.split(r'\[ _ \]', question_text)
            question_data["text"] = [
                {"content": part, "is_gap": bool(re.match(r'\[ _ \]', part))}
                for part in parts
            ]
            question_data["has_gap"] = True

        questions.append(question_data)

    return questions
