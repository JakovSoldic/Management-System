from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Role(models.Model):
    ROLE_CHOICES = (('admin', 'Admin'), ('professor', 'Professor'), ('student', 'Student') )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.get_role_display()

class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True)
    STATUS_CHOICES = (('none', 'None'), ('redovni', 'Redovni'), ('izvanredni', 'Izvanredni') )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)

class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True)
    program = models.TextField()
    points = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    IZBORNI_CHOICES = (('da', 'Da'), ('ne', 'Ne') )
    izborni = models.CharField(max_length=3, choices=IZBORNI_CHOICES)
    carrier = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__role': 'professor'})

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    STATUS_CHOICES = (('upisan', 'Upisan'), ('potpis izgubljen', 'Potpis izgubljen'), ('polozen', 'Položen'))
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)