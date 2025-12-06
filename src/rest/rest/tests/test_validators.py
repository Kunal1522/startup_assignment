import pytest
from rest.validators import TodoValidator
from rest.exceptions import ValidationError


class TestTodoValidator:

    def test_validate_text_success(self):
        result = TodoValidator.validate_text('Valid todo text')
        assert result == 'Valid todo text'

    def test_validate_text_strips_whitespace(self):
        result = TodoValidator.validate_text('  Trimmed text  ')
        assert result == 'Trimmed text'

    def test_validate_text_none_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            TodoValidator.validate_text(None)
        assert 'required' in str(exc_info.value.message).lower()

    def test_validate_text_empty_string_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            TodoValidator.validate_text('')
        assert 'empty' in str(exc_info.value.message).lower()

    def test_validate_text_whitespace_only_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            TodoValidator.validate_text('   ')
        assert 'empty' in str(exc_info.value.message).lower()

    def test_validate_text_non_string_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            TodoValidator.validate_text(123)
        assert 'string' in str(exc_info.value.message).lower()

    def test_validate_text_exceeds_max_length_raises_error(self):
        long_text = 'a' * 501
        with pytest.raises(ValidationError) as exc_info:
            TodoValidator.validate_text(long_text)
        assert 'exceed' in str(exc_info.value.message).lower()

    def test_validate_text_at_max_length_succeeds(self):
        text = 'a' * 500
        result = TodoValidator.validate_text(text)
        assert len(result) == 500
