from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    personal_email = models.EmailField(unique=True, null=True, blank=True)
    locker_number = models.IntegerField(unique=True, default=110, validators=[MinValueValidator(1), MaxValueValidator(200)])
    locker_combination = models.CharField(max_length=20, default="12-12-12")
    good_student = models.BooleanField(default=True)
    classes = models.ManyToManyField("class_app.Class", related_name="students")
    
    def __str__(self):
        return f"{self.name} - {self.student_email} - {self.locker_number}"

    def locker_reassignment(self, new_number):
        self.locker_number = new_number
        self.save()

    def student_status(self, is_good):
        self.good_student = is_good
        self.save()
