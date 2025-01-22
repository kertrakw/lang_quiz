import pytest
from django.test import Client

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def sample_test_data():
    return {
        'title': 'Test 1',
        'type': 'TEXT_INPUT_MEMORY',
        'content': '1. _____ what time does the meeting start?'
    }