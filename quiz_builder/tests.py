from django.test import TestCase
from .parsers import parse_gap_test, parse_choice_test


class ParserTests(TestCase):

    def test_parse_gap_test(self):
        """
        Test parsowania testu z lukami.
        Sprawdza poprawność struktury sparsowanych danych.
        """
        test_content = "1. You need to submit your application [ _ ] advance."
        result = parse_gap_test(test_content)

        # Sprawdzamy czy mamy listę pytań
        self.assertIsInstance(result, list)
        # Sprawdzamy czy mamy pytanie
        self.assertGreater(len(result), 0)
        # Sprawdzamy czy mamy lukę w pytaniu
        self.assertTrue(any(part.get('gap') for part in result[0]))
        # Sprawdzamy strukturę części pytania
        self.assertEqual(len(result[0]), 3)  # tekst przed luką, luka, tekst po luce
        self.assertEqual(result[0][0]['text'], "You need to submit your application ")
        self.assertTrue(result[0][1]['gap'])
        self.assertEqual(result[0][2]['text'], " advance.")

    def test_parse_choice_test(self):
        """
        Test parsowania różnych typów testów wyboru.
        Sprawdza poprawność obsługi SINGLE_CHOICE, MULTIPLE_CHOICE i CHOICE_WITH_GAPS.
        """
        # Test dla SINGLE_CHOICE
        single_choice = (
            "1. Which tense is used to describe your daily routine?\n"
            "A. Present Simple\n"
            "B. Present Continuous\n"
            "C. Past Simple\n"
            "D. Future Simple\n"
            "[A]"
        )
        result = parse_choice_test(single_choice, 'SINGLE_CHOICE')

        self.assertEqual(len(result), 1)  # jedno pytanie
        self.assertEqual(len(result[0]['choices']), 4)  # cztery opcje
        self.assertFalse(result[0].get('has_gap', False))  # nie ma luki
        self.assertFalse(result[0].get('multiple_answers', False))  # pojedynczy wybór

        # Test dla CHOICE_WITH_GAPS
        gap_choice = (
            "1. Have you read the list of [ _ ] that are in this food product?\n"
            "A. recipes\n"
            "B. ingredients\n"
            "C. makings\n"
            "D. elements\n"
            "[B]"
        )
        result = parse_choice_test(gap_choice, 'CHOICE_WITH_GAPS')

        self.assertEqual(len(result), 1)  # jedno pytanie
        self.assertEqual(len(result[0]['choices']), 4)  # cztery opcje
        self.assertTrue(result[0].get('has_gap', False))  # ma lukę
        self.assertIsInstance(result[0]['text'], list)  # tekst jest listą części

        # Test dla MULTIPLE_CHOICE
        multiple_choice = (
            "1. Which of these words can be followed by the suffix \"-less\"?\n"
            "A. hope\n"
            "B. care\n"
            "C. friend\n"
            "D. wonder\n"
            "[A,B,C,D]"
        )
        result = parse_choice_test(multiple_choice, 'MULTIPLE_CHOICE')

        self.assertEqual(len(result), 1)  # jedno pytanie
        self.assertEqual(len(result[0]['choices']), 4)  # cztery opcje
        self.assertTrue(result[0].get('multiple_answers', False))  # wielokrotny wybór


class ViewTests(TestCase):
    def test_home_view(self):
        """Test dostępności strony głównej."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_test_view(self):
        """Test dostępności strony tworzenia testu."""
        response = self.client.get('/test/create/')
        self.assertEqual(response.status_code, 200)
