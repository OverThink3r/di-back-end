from django.db import models


# Create your models here.
class User(models.Model):
  email = models.CharField(max_length=255, unique=True)
  name = models.CharField(max_length=255)
  password = models.CharField(max_length=255)


class Book(models.Model):
    author = models.CharField(max_length=255, null=False)
    isbn = models.CharField(max_length=255, null=False)
    release_date = models.DateTimeField(null=False)
    title = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
