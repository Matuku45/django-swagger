from django.db import models

# Create your models here.
class PersonModel(models.Model):
    name = models.CharField(max_length=200)
    lastname = models.CharField(max_length= 300)
