# Changelog
All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-01-22
### Added
- Basic test types (TEXT_INPUT_MEMORY, TEXT_INPUT_WORDLIST)
- Test parser for different formats
- Test creation form
- Test preview functionality

### Changed
- Updated test type detection logic
- Improved form validation

### Fixed
- Parser handling of multiline tests
- Form display issues with word list field

## [Unreleased]
### Planned
- Test saving functionality
- Tag system
- User authentication
- API endpoints

## [0.2.0] - 2025-01-24
### Added
- Obsługa różnych formatów oznaczeń odpowiedzi (a), A., 1), -)
- Automatyczna konwersja formatów na standardowy (A., B., C., D.)

### Changed
- Poprawiono obsługę testu typu MULTIPLE_CHOICE
- Zmieniono sposób wykrywania typu testu w preview (użycie typu z sesji)

### Fixed
- Naprawiono wyświetlanie właściwych kontrolek dla MULTIPLE_CHOICE (checkboxy zamiast radio buttons)

## [0.2.1] - 2025-01-25
### Added
- Single answer validation for non-multiple choice tests
- Detailed validation feedback for answers

### Changed
- Translated all validation error messages to English
- Improved error message display in form interface

### Fixed
- Validation for duplicate answers in multiple choice tests
- Form error messages display
- Answer count validation for different test types

## [0.2.2] - 2025-01-26
### Added
- Question number cleaning functionality
- Single answer validation for non-multiple choice tests

### Changed
- Translated all validation error messages to English
- Improved error message display in form interface

### Fixed
- Validation for duplicate answers in multiple choice tests
- Form error messages display
- Answer count validation for different test types

## [Unreleased]
### Changed
- Modified CHOICE_WITH_GAPS test display
  - Replaced select with radio buttons for answer options
  - Added placeholder (_______) in gap location
  - Implemented selected answer display in gap
  - Updated JavaScript to handle radio button selection