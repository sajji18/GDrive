from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Folder(models.Model): # model to represent folders by users
    name = models.CharField(max_length=55)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(default="Add Description")
    parent_id = models.BigIntegerField(default=-1)
    is_public = models.BooleanField(default=True)
    # parent_folder = models.ForeignKey(
    #     'self', 
    #     null=True, 
    #     blank=True, 
    #     related_name='child_folders', 
    #     on_delete=models.CASCADE
    # )
    def __str__(self):
        return f'{self.name} (Owner: {self.owner.username})'

class FolderRelationTable (models.Model):
    parent = models.ForeignKey(Folder, related_name="parent", on_delete=models.CASCADE)
    child = models.ForeignKey(Folder, related_name="child", on_delete=models.CASCADE)
    class Meta:
        unique_together = ('parent', 'child')
    def __str__(self):
        return f'{self.parent} -> {self.child}'

class File(models.Model):
    filetitle = models.CharField(max_length=55, default="File")
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file = models.FileField(upload_to="Files")
    
    def __str__(self):
        return f'{self.filetitle} in {self.folder}'

