# Language Quiz Platform

A Django application for creating and managing language learning tests.

## Features
- Multiple test types (gap filling, word choice, single/multiple choice)
- Automatic test parsing from text input
- Test preview and validation
- Test categorization with tags
- Multiple test types (gap filling, word choice, single/multiple choice)
- Automatic test parsing from text input
- Test preview and validation
- Test categorization with tags
- Support for various answer formats (A., a), 1), -)
- Automatic format standardization

## Requirements
- Python 3.11+
- Django 4.2 LTS
- Bootstrap 5.3

## Quick Start
1. Clone repository
2. Create virtual environment:
python -m venv venv
source venv/bin/activate  # (Linux/Mac) or venv\Scripts\activate (Windows)
3. Install dependencies:
pip install -r requirements.txt
4. Run migrations:
python manage.py migrate
5. Start development server:
python manage.py runserver