from typing import Optional
from ..exceptions import ValidationError


class TodoValidator:
    MIN_LENGTH: int = 1
    MAX_LENGTH: int = 500

    @classmethod
    def validate_text(cls, text: any) -> str:
        if text is None:
            raise ValidationError('Text is required')
        
        if not isinstance(text, str):
            raise ValidationError('Text must be a string')
        
        cleaned = text.strip()
        
        if len(cleaned) < cls.MIN_LENGTH:
            raise ValidationError('Text cannot be empty')
        
        if len(cleaned) > cls.MAX_LENGTH:
            raise ValidationError(
                f'Text cannot exceed {cls.MAX_LENGTH} characters',
                details={'max_length': cls.MAX_LENGTH, 'current_length': len(cleaned)}
            )
        
        return cleaned
