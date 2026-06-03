from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    grade = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=15)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        