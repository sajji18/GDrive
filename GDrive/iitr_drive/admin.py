from django.contrib import admin
from .models import Folder

# Register your models here.
@admin.register(Folder)
class AdminFolder(admin.ModelAdmin):
    list_display = ('name', 'owner')
