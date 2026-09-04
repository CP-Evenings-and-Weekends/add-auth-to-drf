from django.test import TestCase, Client
from django.urls import reverse
from tests.answers import all_classes, all_students, a_student, a_class
import json

class Test_endpoints(TestCase):

    fixtures = [
        'tests/fixtures/classes.json',
        'tests/fixtures/students.json',
        'tests/fixtures/grades.json'
    ]

    def setUp(self):
        client = Client()
    # V
    def test_001_all_classes(self):
        response = self.client.get(reverse('all_classes'))
        with self.subTest():
            self.assert_(response.status_code == 200)
        content = json.loads(response.content)
        self.assertEquals(content, all_classes)

    def test_002_all_students(self):
        response = self.client.get(reverse('all_students'))
        with self.subTest():
            self.assert_(response.status_code == 200)
        content = json.loads(response.content)
        self.assertEquals(content, all_students)

    # VI
    def test_003_a_student(self):
        response = self.client.get(reverse('a_student', args=[1]))
        with self.subTest():
            self.assert_(response.status_code == 200)
        content = json.loads(response.content)
        self.assertEquals(content, a_student)
    
    def test_004_a_class_by_subject(self):
        response = self.client.get(reverse('a_class', args=['python']))
        with self.subTest():
            self.assert_(response.status_code == 200)
        content = json.loads(response.content)
        self.assertEquals(content, a_class)

    def test_005_a_student_does_not_exist_returns_404(self):
        response = self.client.get(reverse('a_student', args=[52]))
        self.assert_(response.status_code==404)

    def test_006_a_class_does_not_exist_returns_404(self):
        response = self.client.get(reverse('a_class', args=['15']))
        self.assert_(response.status_code==404)

    
        


        

    
        


        