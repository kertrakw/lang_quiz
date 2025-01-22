import re

def detect_test_type(content):
    """
    Wykrywa typ testu na podstawie jego zawartości
    """
    # Jeśli znajdziemy "A.", "B.", "C." - to jest test wyboru
    has_choices = bool(re.search(r'\n[A-D]\.', content))
    
    # Jeśli znajdziemy lukę (_____) - to jest test z lukami
    has_gaps = bool(re.findall(r'_{3,}', content))
    
    # Jeśli mamy oba elementy i luka jest w głównym tekście (nie w opcjach)
    # to jest test wyboru z lukami do uzupełnienia
    if has_choices and has_gaps:
        # Sprawdzamy czy luka jest w głównym tekście pytania
        paragraphs = content.split('\n')
        for p in paragraphs:
            if p.strip() and not p.startswith(('A.', 'B.', 'C.', 'D.')):
                if '____' in p:
                    return 'CHOICE_WITH_GAPS'
    
    if has_choices:
        return 'MULTIPLE_CHOICE'
    
    if has_gaps:
        return 'TEXT_INPUT'
        
    return None

def parse_gap_test(content):
    """
    Parsuje test z lukami (zarówno jednolinijkowy jak i wielolinijkowy)
    """
    # Dzielimy na linijki
    lines = content.split('\n')
    questions = []
    
    for line in lines:
        if not line.strip():  # Pomijamy puste linie
            continue
            
        # Znajdujemy wszystkie luki w linii
        parts = re.split(r'(_{3,})', line)
        
        current_question = []
        for i, part in enumerate(parts):
            if re.match(r'_{3,}', part):  # Jeśli to luka
                current_question.append({
                    "text": "",
                    "gap": True,
                    "id": len(questions) + 1
                })
            else:
                current_question.append({
                    "text": part,
                    "gap": False
                })
        
        questions.append(current_question)
    
    return questions

def parse_choice_test(content):
    """
    Parsuje test wyboru (zarówno z pytaniami jak i z lukami)
    """
    # Dzielimy na pytania (według numeracji lub pustych linii)
    questions_raw = re.split(r'\n\s*\n|\n(?=\d+\.)', content.strip())
    questions = []
    
    for q_raw in questions_raw:
        if not q_raw.strip():  # Pomijamy puste
            continue
            
        # Dzielimy na pytanie i odpowiedzi
        parts = q_raw.split('\n')
        question_text = parts[0].strip()
        
        # Znajdujemy odpowiedzi
        choices = []
        for part in parts[1:]:
            if re.match(r'[A-D]\.', part.strip()):
                choice_text = part[2:].strip()  # Usuwamy "A." itp.
                choices.append({
                    "text": choice_text,
                    "letter": part[0]
                })
        
        # Sprawdzamy czy pytanie ma lukę
        has_gap = '____' in question_text
        
        questions.append({
            "text": question_text,
            "has_gap": has_gap,
            "choices": choices,
            "id": len(questions) + 1
        })
    
    return questions