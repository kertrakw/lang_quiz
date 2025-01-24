# Development Guide

## Project Structure
- `quiz_builder/`: Main application code
  - `parsers.py`: Test parsing logic
  - `models.py`: Database models
  - `views.py`: View controllers
  - `templates/`: HTML templates

## Coding Standards
- Comments in Polish
- User interface in English
- Follow PEP 8
- Use docstrings for functions/classes

## Input Formats
The application accepts various formats for answer options:
- Letters with dot: A., B., C., D.
- Letters with parenthesis: A), B), C), D)
- Lowercase letters: a., b., c., d.
- Numbers: 1., 2., 3., 4.
- Dashes: -

All formats are automatically converted to standard format (A., B., C., D.)

## Test Types
1. TEXT_INPUT_MEMORY: Free text input
2. TEXT_INPUT_WORDLIST: Selection from word list
3. SINGLE_CHOICE: Single answer selection
4. MULTIPLE_CHOICE: Multiple answers selection
   - Supports multiple answer formats
   - Uses checkboxes for selection
5. CHOICE_WITH_GAPS: Coming soon

## Development Setup
1. Configure environment variables
2. Install development dependencies
3. Run tests: `python manage.py test`

## Common Development Tasks
- Adding new test type
- Modifying parser logic
- Adding new template