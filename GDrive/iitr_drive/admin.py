from django.contrib import admin
from .models import Folder, File, FolderRelationTable

# Register your models here.
@admin.register(Folder)
class AdminFolder(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'description']

@admin.register(File)
class AdminFile(admin.ModelAdmin):
   list_display = ('id','file','filetitle')
   
@admin.register(FolderRelationTable)
class AdminFolderRelationTable(admin.ModelAdmin):
    list_display = ['parent', 'child']