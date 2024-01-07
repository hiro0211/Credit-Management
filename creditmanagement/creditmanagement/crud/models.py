from django.db import models
from django.urls import reverse 
from django.conf import settings

class Category(models.Model):
  name = models.CharField(max_length=200)
  requiredment_credit = models.PositiveIntegerField(default=0)
  
  def __str__(self):
    return self.name

class Subject(models.Model):
  name = models.CharField(max_length=100) 
  credit = models.FloatField(null=True, blank=False)
  score = models.PositiveIntegerField()
  category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
    return reverse('list')
  
class ParentCategory(models.Model):
  name = models.CharField(max_length=200)
  parent = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
  required_credit = models.FloatField(null=True, blank=False)
  

"""
class Student(models.Model):
  name = models.CharField(max_length=100)
  subjects = models.ManyToManyField(Subject)
  """