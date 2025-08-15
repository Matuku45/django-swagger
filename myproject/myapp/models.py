from django.db import models

class PersonModel(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # hashed password
    agree_terms = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.email})"
