from django.db import models
from django.core.validators import ValidationError
#from customauth.models import *

def restrict_subjects(value):
    if TeachingSubject.objects.filter(teacher=value).count() > 5:
        raise ValidationError('A teacher can only teach 5 subjects')

class Subject(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Teacher(models.Model):
    #attributes
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to = 'uploads/', default='uploads/default.png')
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(unique = True, null = False, blank = False, max_length=25)
    room_number = models.CharField(max_length=20)
    
    def __str__(self):
        return self.first_name+" "+self.last_name

class TeachingSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,validators=(restrict_subjects, ), on_delete=models.CASCADE)