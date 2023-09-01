from django.shortcuts import render, redirect, get_object_or_404
from .forms import FolderForm
from .models import Folder
from django.urls import reverse

def folder_list(request):
    context = {
        'folders': Folder.objects.all()
    }
    return render(request, 'iitr_drive/folder_list.html', context)


def folder_detail(request, folderid):
    if request.user.is_authenticated:
        folder = get_object_or_404(Folder, id=folderid)
        context = {'folder': folder}
        return render(request, 'iitr_drive/folder.html', context)
    else:
        return redirect('login')


def add_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.owner = request.user
            folder.save()
            return redirect('folder_list')  # Redirect to the folder list page
    else:
        form = FolderForm()
    
    return render(request, 'iitr_drive/add_folder.html', {'form': form})
