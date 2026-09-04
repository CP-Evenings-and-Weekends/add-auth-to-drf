from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Student
from .serializers import StudentSerializer
from django.shortcuts import get_object_or_404

class StudentList(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value

class StudentList(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetail(RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_object(self):
        id_or_name = int_or_str(self.kwargs["id_or_name"])
        if isinstance(id_or_name, int):
            return Student.objects.get(pk=id_or_name)
        return get_object_or_404(Student, name=id_or_name)
    
    