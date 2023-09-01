from django.shortcuts import render, redirect, get_object_or_404
from .forms import FolderForm
from .models import Folder, File
from django.urls import reverse

def folder_list(request):
    context = {
        'folders': Folder.objects.all()
    }
    return render(request, 'iitr_drive/folder_list.html', context)


def folder_detail(request, folderid):
    if request.user.is_authenticated:
        folder_user = Folder.objects.get(id=folderid)
        files = File.objects.filter(folder=folder_user)
        context = {'folderid':folderid,'files':files}
        
        if request.method == 'POST':
            file_user = request.FILES.get('file')
            file_title = request.POST.get('filetitle')
            fileadd = File.objects.create(filetitle=file_title,file=file_user,folder=folder_user)

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
