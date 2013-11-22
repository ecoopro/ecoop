from django.db import models

# Create your models here.

class Model1(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    choice_text = models.CharField(max_length=4)
    votes = models.IntegerField(default=0)

