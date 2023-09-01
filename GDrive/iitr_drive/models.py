from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Folder(models.Model): # model to represent folders by users
    name = models.CharField(max_length=55)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(default="Add Description")
    linked_in = models.BigIntegerField(default=-1)
    
    def __str__(self):
        return f'{self.name} (Owner: {self.owner.username})'

    
class File(models.Model):
    filetitle = models.CharField(max_length=55)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file = models.FileField(upload_to="Files")
    
    def __str__(self):
        return f'{self.filetitle} in {self.folder}'

