from django.contrib import admin
from .models import Folder, File

# Register your models here.
@admin.register(Folder)
class AdminFolder(admin.ModelAdmin):
    list_display = ['name', 'owner', 'description']

@admin.register(File)
class Adminfolder(admin.ModelAdmin):
   list_display = ('id','file','filetitle')