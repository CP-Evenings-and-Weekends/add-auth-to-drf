from django.db import models
from .validators import validate_subject_format, validate_professor_name


class Class(models.Model):
    subject = models.CharField(
        max_length=100,
        unique=True,
        validators=[validate_subject_format]
    )

    professor = models.CharField(
        max_length=100,
        default="Professor Chan",
        validators=[validate_professor_name]
    )