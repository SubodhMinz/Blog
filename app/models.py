from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Blog(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    photo = models.ImageField(upload_to='image')