from django.db import models
from django.urls import reverse 
from django.conf import settings

class Category(models.Model):
  name = models.CharField(max_length=200, verbose_name="科目カテゴリ")
  requiredment_credit = models.PositiveIntegerField(default=0)
  
  def __str__(self):
    return self.name

class Subject(models.Model):
  name = models.CharField(max_length=100, verbose_name="科目名") 
  credit = models.FloatField(null=True, blank=False, verbose_name="単位数", default=2.0)
  score = models.PositiveIntegerField(verbose_name="得点")
  category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name="科目カテゴリ")
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