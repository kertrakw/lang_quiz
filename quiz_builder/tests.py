from django.test import TestCase
from .parsers import detect_test_type, parse_gap_test, parse_choice_test


class ParserTests(TestCase):
    def test_detect_test_type(self):
        # Test dla TEXT_INPUT_MEMORY
        gap_test = "1. _________ what time does the meeting start?"
        # Test dla SINGLE_CHOICE
        choice_test = "1. Question\nA. First\nB. Second\n[A]"
        # Test dla CHOICE_WITH_GAPS
        gap_choice_test = "Complete: _____\nA. this\nB. that\n[A]"
        # Test dla MULTIPLE_CHOICE
        multiple_choice = "1. Question\nA. First\nB. Second\n[A,B]"
        # Test dla TEXT_INPUT_WORDLIST
        wordlist_test = "IN - ON - AT\n1. _________ what time?"

        self.assertEqual(detect_test_type(gap_test), 'TEXT_INPUT_MEMORY')
        self.assertEqual(detect_test_type(choice_test), 'SINGLE_CHOICE')
        self.assertEqual(detect_test_type(gap_choice_test), 'CHOICE_WITH_GAPS')
        self.assertEqual(detect_test_type(multiple_choice), 'MULTIPLE_CHOICE')
        self.assertEqual(detect_test_type(wordlist_test), 'TEXT_INPUT_WORDLIST')

    def test_parse_gap_test(self):
        test_content = "1. _________ what time?"
        result = parse_gap_test(test_content)

        # Sprawdzamy czy mamy listę pytań
        self.assertIsInstance(result, list)
        # Sprawdzamy czy mamy pytanie
        self.assertGreater(len(result), 0)
        # Sprawdzamy czy mamy lukę w pytaniu
        self.assertTrue(any(part.get('gap') for part in result[0]))

    def test_parse_choice_test(self):
        # Test dla SINGLE_CHOICE
        single_choice = "1. Question\nA. First\nB. Second\n[A]"
        result = parse_choice_test(single_choice, 'SINGLE_CHOICE')

        self.assertEqual(len(result), 1)  # jedno pytanie
        self.assertEqual(len(result[0]['choices']), 2)  # dwie opcje
        self.assertFalse(result[0].get('has_gap', False))  # nie ma luki
        self.assertFalse(result[0].get('multiple_answers', False))  # pojedynczy wybór

        # Test dla CHOICE_WITH_GAPS
        gap_choice = "Complete: _____\nA. this\nB. that\n[A]"
        result = parse_choice_test(gap_choice, 'CHOICE_WITH_GAPS')

        self.assertEqual(len(result), 1)  # jedno pytanie
        self.assertEqual(len(result[0]['choices']), 2)  # dwie opcje
        self.assertTrue(result[0].get('has_gap', False))  # ma lukę
        self.assertIsInstance(result[0]['text'], list)  # tekst jest listą części

        # Test dla MULTIPLE_CHOICE
        multiple_choice = "1. Question\nA. First\nB. Second\n[A,B]"
        result = parse_choice_test(multiple_choice, 'MULTIPLE_CHOICE')

        self.assertEqual(len(result), 1)  # jedno pytanie
        self.assertEqual(len(result[0]['choices']), 2)  # dwie opcje
        self.assertTrue(result[0].get('multiple_answers', False))  # wielokrotny wybór


class ViewTests(TestCase):
    def test_home_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_test_view(self):
        response = self.client.get('/test/create/')
        self.assertEqual(response.status_code, 200)
