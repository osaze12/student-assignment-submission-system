# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Student(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matric_no = models.CharField(default='empty', max_length=10)
    course_of_study = models.CharField(max_length=100)

    @receiver(post_save, sender=User)
    def update_user_student(sender, instance, created, **kwargs):
        if created:
            Student.objects.create(user=instance)
        instance.student.save()


    def __str__(self):
        return '{} \n{}\n'.format(self.user, self.matric_no)
      
      
class Submission_datetime(models.Model):
    from_datetime = models.DateTimeField(null=True,blank=True)
    to_datetime = models.DateTimeField(blank=True, null=True)
    

class Teacher(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    code = models.CharField(max_length=10) 
    course_code = models.CharField(max_length=10)
    pd = models.ManyToManyField(Student, through='Pdf_file')
    from_datetime = models.DateTimeField(null=True,blank=True)
    to_datetime = models.DateTimeField(blank=True, null=True)
    

    def __str__(self):
        return self.last_name




class Pdf_file(models.Model):
    lecturer = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    document = models.FileField(upload_to='uploads/%Y/%m/%d')
    point = models.IntegerField(default=0)
    gradd = models.CharField(default='No Grade yet', max_length=100)
    graded = models.BooleanField(default=False) 
    

    def __str__(self):
      return str(self.document)
   

