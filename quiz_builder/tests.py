from django.test import TestCase
from .parsers import detect_test_type, parse_gap_test, parse_choice_test

class ParserTests(TestCase):
    def test_detect_test_type(self):
        gap_test = "1. _________ what time does the meeting start?"
        choice_test = "1. Question\nA. First\nB. Second"
        gap_choice_test = "Complete: _____\nA. this\nB. that"
        
        self.assertEqual(detect_test_type(gap_test), 'TEXT_INPUT')
        self.assertEqual(detect_test_type(choice_test), 'MULTIPLE_CHOICE')
        self.assertEqual(detect_test_type(gap_choice_test), 'CHOICE_WITH_GAPS')

    def test_parse_gap_test(self):
        test_content = "1. _________ what time?"
        result = parse_gap_test(test_content)
        self.assertTrue(any(part['gap'] for part in result[0]))

    def test_parse_choice_test(self):
        test_content = "1. Question\nA. First\nB. Second"
        result = parse_choice_test(test_content)
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]['choices']), 2)

class ViewTests(TestCase):
    def test_home_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_test_view(self):
        response = self.client.get('/test/create/')
        self.assertEqual(response.status_code, 200)