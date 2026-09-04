from django.core.exceptions import ValidationError


def validate_subject_format(value):
    if value != value.title():
        raise ValidationError("Subject must be in title case format.")


def validate_professor_name(value):
    parts = value.split()

    if len(parts) != 2 or parts[0] != "Professor" or not parts[1].istitle():
        raise ValidationError(
            'Professor name must be in the format "Professor Murdock".'
        )