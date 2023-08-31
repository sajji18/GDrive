from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Folder(models.Model): # model to represent folders by users
    name = models.CharField(max_length=55)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(default="Add Description")
    
    def __str__(self):
        return f'{self.name} | {self.owner}'
