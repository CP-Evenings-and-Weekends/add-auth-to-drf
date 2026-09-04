from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Grade(models.Model):
    grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )

    a_class = models.ForeignKey(
        "class_app.Class",
        on_delete=models.CASCADE
    )

    student = models.ForeignKey(
        "student_app.Student",
        on_delete=models.CASCADE
    )
    
    