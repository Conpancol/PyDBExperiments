from django.db import models


class User(models.Model):
    username = models.EmailField(max_length=60, blank=True)
    password = models.CharField(max_length=20)
