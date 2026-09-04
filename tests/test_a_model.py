from django.test import TestCase
from student_app.models import Student
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.utils import DataError
from class_app.models import Class
from grade_app.models import Grade

# Create your tests here.


## PART I
class Test_student(TestCase):
    def setUp(self):
        Student.objects.create(
            name="Johnny H. Harris",
            student_email="thisIsMyEmail@school.com",
            personal_email="thisIsMyEmail@gmail.com",
            locker_number=108,
            locker_combination="11-11-11",
            good_student=False,
        )
        Class.objects.create(subject="Python", professor="Mrs. Zaynab")

    def test_001_student_with_improper_good_student_field(self):
        try:
            new_student = Student.objects.create(
                name="John W. Watson",
                student_email="thisIsAnEmail@school.com",
                personal_email="thisIsAnEmail@gmail.com",
                locker_number=13,
                locker_combination="12-33-44",
                good_student=None,
            )

            new_student.full_clean()
            self.fail()
        except IntegrityError as e:
            # print(e)
            self.assertIn(
                'null value in column "good_student" of relation "student_app_student" violates not-null constraint',
                str(e),
            )

    def test_002_student_with_improper_email_fields(self):
        try:
            new_student = Student.objects.create(
                name="John W. Watson",
                student_email="thisIsNotAnEmail",
                personal_email=False,
                locker_number=13,
                locker_combination="23-33-44",
                good_student=True,
            )
            new_student.full_clean()
            self.fail()
        except ValidationError as e:
            # print(e.message_dict)
            self.assert_(
                "student_email" in e.message_dict and "personal_email" in e.message_dict
            )

    def test_003_student_with_improper_locker_number_fields(self):
        try:
            new_student = Student.objects.create(
                name="John W. Watson",
                student_email="thisIsAnEmail@school.com",
                personal_email="thisIsAnEmail@gmail.com",
                locker_number="None",
                locker_combination="23-33-44",
                good_student=True,
            )
            new_student.full_clean()
            self.fail()
        except Exception as e:
            # print(e)
            self.assert_(
                "Field 'locker_number' expected a number but got 'None'" in str(e)
            )

    def test_004_student_with_improper_locker_combination_fields(self):
        try:
            new_student = Student.objects.create(
                name="John W. Watson",
                student_email="thisIsAnEmail@school.com",
                personal_email="thisIsAnEmail@gmail.com",
                locker_number=13,
                locker_combination=None,
                good_student=True,
            )
            new_student.full_clean()
            self.fail()
        except IntegrityError as e:
            # print(e)
            self.assert_('null value in column "locker_combination" ' in str(e))

    def test_005_student_with_improper_name_field(self):
        try:
            new_student = Student.objects.create(
                name=None,
                student_email="thisIsAnEmail@school.com",
                personal_email="thisIsAnEmail@gmail.com",
                locker_number=13,
                locker_combination="12-12-12",
                good_student=True,
            )
            new_student.full_clean()
            self.fail()
        except Exception as e:
            # print(e)
            self.assert_('null value in column "name" ' in str(e))

    def test_006_student_with_proper_fields(self):
        new_student = Student.objects.create(
            name="John W. Wally",
            student_email="john@school.com",
            personal_email="john@gmail.com",
            locker_number=13,
            locker_combination="12-12-12",
            good_student=True,
        )
        new_student.save()
        new_student.classes.add(6)
        new_student.full_clean()
        self.assertIsNotNone(new_student)

    # PART II

    def test_007_student_with_repeated_student_email(self):
        try:
            new_student = Student.objects.create(
                name="Johnny H. Harris",
                student_email="thisIsMyEmail@school.com",
                personal_email="myEmail@gmail.com",
                locker_number=109,
                locker_combination="11-11-11",
                good_student=False,
            )
            new_student.full_clean()
            self.fail()
        except IntegrityError as e:
            # print(e)
            self.assert_("student_app_student_student_email_key" in str(e))

    def test_008_student_with_repeated_personal_email(self):
        try:
            new_student = Student.objects.create(
                name="Johnny H. Harris",
                student_email="IsMyEmail@school.com",
                personal_email="thisIsMyEmail@gmail.com",
                locker_number=109,
                locker_combination="11-11-11",
                good_student=False,
            )
            new_student.full_clean()
            self.fail()
        except IntegrityError as e:
            # print(e)
            self.assert_("student_app_student_personal_email_key" in str(e))

    def test_009_student_with_repeated_locker_number(self):
        try:
            new_student = Student.objects.create(
                name="Johnny H. Harris",
                student_email="IsyEmail@school.com",
                personal_email="tIsMyEmail@gmail.com",
                locker_number=108,
                locker_combination="11-11-11",
                good_student=False,
            )
            new_student.full_clean()
            self.fail()
        except IntegrityError as e:
            # print(e)
            self.assert_("student_app_student_locker_number" in str(e))

    def test_010_student_utilizing_default_values(self):
        new_student = Student.objects.create(
            name="Maverick H. Macconnel",
            student_email="mav@school.com",
            personal_email="mav@gmail.com",
        )
        new_student.save()
        new_student.classes.add(10)
        new_student.full_clean()
        self.assertIsNotNone(new_student)

    ## PART III

    def test_011_student_with_improper_name_format(self):
        try:
            new_student = Student.objects.create(
                name="Maverick Macconnel",
                student_email="mav@school.com",
                personal_email="mav@gmail.com",
            )
            new_student.full_clean()
            self.fail()
        except ValidationError as e:
            # print(e.message_dict)
            self.assert_(
                'Name must be in the format "First Middle Initial. Last"'
                in e.message_dict["name"]
            )

    def test_012_student_with_improper_student_email(self):
        try:
            new_student = Student.objects.create(
                name="Maverick H. Macconnel",
                student_email="mav@school.org",
                personal_email="mav@gmail.com",
            )
            new_student.full_clean()
            self.fail()
        except ValidationError as e:
            # print(e.message_dict)
            self.assert_(
                "Email must be from school domain" in e.message_dict["student_email"]
            )

    def test_013_student_with_improper_locker_combination(self):
        try:
            new_student = Student.objects.create(
                name="Maverick H. Macconnel",
                student_email="mav@school.com",
                personal_email="mav@gmail.com",
                locker_combination="zz-234-p1",
            )
            new_student.full_clean()
            self.fail()
        except ValidationError as e:
            # print(e.message_dict)
            self.assert_(
                'Combination must be in the format "12-12-12"'
                in e.message_dict["locker_combination"]
            )

    def test_014_student_with_low_locker_number(self):
        try:
            new_student = Student.objects.create(
                name="Maverick H. Macconnel",
                student_email="mav@school.com",
                personal_email="mav@gmail.com",
                locker_number=0,
            )
            new_student.full_clean()
            self.fail()
        except ValidationError as e:
            # print(e.message_dict)
            self.assert_(
                "Ensure this value is greater than or equal to 1."
                in e.message_dict["locker_number"]
            )

    def test_015_student_with_high_locker_number(self):
        try:
            new_student = Student.objects.create(
                name="Maverick H. Macconnel",
                student_email="mav@school.com",
                personal_email="mav@gmail.com",
                locker_number=350,
            )
            new_student.full_clean()
            self.fail()
        except ValidationError as e:
            # print(e.message_dict)
            self.assert_(
                "Ensure this value is less than or equal to 200."
                in e.message_dict["locker_number"]
            )

    # PART IV

    def test_016_student_missing_classes(self):
        try:
            new_student = Student.objects.create(
                name="Maverick H. Macconnel",
                student_email="mav@school.com",
                personal_email="mav@gmail.com",
            )
            new_student.full_clean()
            self.fail()
        except ValidationError as e:
            self.assert_(
                "A student must be enrolled in between 1 and 7 classes."
                in e.message_dict["__all__"]
            )

    def test_017_student_with_too_many_classes(self):
        try:
            new_student = Student.objects.create(
                name="Maverick H. Macconnel",
                student_email="mav@school.com",
                personal_email="mav@gmail.com",
            )
            new_student.save()
            for idx in range(9):
                a_class = Class.objects.create(
                    subject=f"Python{idx}", professor="Mrs. Ana"
                )
                a_class.save()
                new_student.classes.add(a_class.id)
            new_student.full_clean()
            self.fail()
        except ValidationError as e:
            # print(e.message_dict)
            self.assert_(
                "A student must be enrolled in between 1 and 7 classes."
                in e.message_dict["__all__"]
            )

    def test_018_Class_with_improper_subject_format(self):
        try:
            a_class = Class.objects.create(
                subject="a subject", professor="Professor Ben"
            )
            a_class.save()
            a_class.add_a_student(Student.objects.all().first().id)
            a_class.full_clean()
            self.fail()
        except ValidationError as e:
            # print(e.message_dict)
            self.assert_(
                "Subject must be in title case format." in e.message_dict["subject"]
            )

    def test_019_Class_with_improper_professor_format(self):
        try:
            a_class = Class.objects.create(subject="Math", professor="Mr. Ben")
            a_class.save()
            a_class.add_a_student(Student.objects.all().first().id)
            a_class.full_clean()
            self.fail()
        except ValidationError as e:
            # print(e.message_dict)
            self.assert_(
                'Professor name must be in the format "Professor Adam".'
                in e.message_dict["professor"]
            )

    def test_020_Class_with_not_enough_students(self):
        try:
            a_class = Class.objects.create(subject="Math", professor="Professor Ben")
            a_class.save()
            a_class.full_clean()
            self.fail()
        except ValidationError as e:
            # print(e)
            self.assert_(
                "A class must have between 1 and 30 students"
                in e.message_dict["__all__"]
            )

    def test_021_Grade_with_proper_input(self):
        grade = Grade.objects.create(
            grade=98.75,
            a_class=Class.objects.all().first(),
            student=Student.objects.all().first(),
        )
        grade.full_clean()
        self.assertIsNotNone(grade)

    def test_022_Grade_with_high_grade(self):
        try:
            grade = Grade.objects.create(
                grade=198.75,
                a_class=Class.objects.all().first(),
                student=Student.objects.all().first(),
            )
            grade.full_clean()
            self.fail()
        except ValidationError as e:
            # print(e)
            self.assert_('Ensure this value is less than or equal to 100.0.' in e.message_dict['grade'])


    def test_023_Grade_with_incorrect_grade_format(self):
        try:
            grade = Grade.objects.create(
                grade=1598.756,
                a_class=Class.objects.all().first(),
                student=Student.objects.all().first(),
            )
            grade.full_clean()
            self.fail()
        except DataError as e:
            # print(e)
            self.assert_('numeric field overflow' in str(e))
