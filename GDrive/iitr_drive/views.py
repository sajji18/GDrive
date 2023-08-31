from django.shortcuts import render, redirect
from .forms import FolderForm
from .models import Folder
from django.urls import reverse

def folder(request):
    context = {
        'folders': Folder.objects.all()
    }
    return render(request, 'iitr_drive/folders.html', context)


def add_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.owner = request.user
            folder.save()
            return redirect('folders')  # Redirect to the folder list page
    else:
        form = FolderForm()
    
    return render(request, 'iitr_drive/add_folder.html', {'form': form})
