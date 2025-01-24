# API Endpoints Documentation

## Tests

### GET /api/tests/
Returns list of all tests.

Response: List of test objects

### POST /api/tests/
Creates a new test.

Request body:
```json
{
    "title": "string",
    "test_type": "string",
    "content": "string",
    "word_list": "string" (optional)
}
```

### Notes
`test_type`: one of:
  - TEXT_INPUT_MEMORY
  - TEXT_INPUT_WORDLIST
  - SINGLE_CHOICE
  - MULTIPLE_CHOICE
  - CHOICE_WITH_GAPS

`content`: supports various formats for options:
  - A., B., C., D.
  - a), b), c), d)
  - 1., 2., 3., 4.
  - dashes (-)
  - answers in square brackets at the end [A,C]

### GET /api/tests/<id>/
Returns details of specific test.

### PUT /api/tests/<id>/
Updates existing test.

Request body: same as POST /api/tests/

### DELETE /api/tests/<id>/
Deletes specific test.

## Categories

### GET /api/tests/categories/
Returns list of test categories.

### POST /api/tests/categories/
Creates new category.

## Search

### GET /api/tests/search/?query=<term>&category=<category>
Searches for tests by term and/or category.

## Test Results

### POST /api/tests/<id>/check-answers/
Checks user's answers for specific test.

### GET /api/tests/<id>/results/
Returns test results.