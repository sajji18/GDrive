from django.shortcuts import render, redirect, get_object_or_404
from .forms import FolderForm
from django.contrib.auth.decorators import login_required
from .models import Folder, File, FolderRelationTable
from django.urls import reverse
import qrcode
from io import BytesIO
from PIL import Image
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid

@login_required
def folder_list(request):
    current_user = request.user
    folders = Folder.objects.filter(owner=current_user, parent_id=-1)
    print(folders)
    context = {
        'folders': folders,
    }
    return render(request, 'iitr_drive/folder_list.html', context)


def folder_detail(request, folderid):
    if request.user.is_authenticated:
        current_folder = get_object_or_404(Folder, id=folderid)
        children_records = FolderRelationTable.objects.filter(parent=current_folder)
        child_folders = [record.child for record in children_records]
        files = File.objects.filter(folder=current_folder)
        context = {
            'folderid': folderid,
            'files': files,
            'child_folders': child_folders
        }
        if request.method == 'POST':
            if 'file' in request.FILES:
                file_user = request.FILES['file']
                file_title = request.POST.get('filetitle')
                if file_title:
                    fileadd = File.objects.create(filetitle=file_title, file=file_user, folder=current_folder)
                    fileadd.save()
        return render(request, 'iitr_drive/folder.html', context)
    else:
        return redirect('login')


@csrf_exempt
def add_folder(request):
    if request.method == 'POST':
        folder_name = request.POST['folder_name']
        description = request.POST['folder_description']
        parent_id = (request.POST['folder_parent_id'])
        if folder_name:  
            owner = request.user
            new_folder = Folder(name=folder_name, description=description, owner=owner)
            new_folder.save()
            if parent_id not in ['None', '-1']:
                parent_id = int(parent_id)
                parent_child_record = FolderRelationTable(
                    parent_id=parent_id, 
                    child_id=new_folder.id
                )       
                parent_child_record.save()
                new_folder.parent_id = parent_id
                new_folder.save()
            print("Folder saved successfully.")
            return redirect('folder_list')
        else: 
            return JsonResponse({ 'message': "Folder Name is Required" })
    elif request.method == 'GET':
        parent_id = request.GET.get('parent_id')
        if parent_id == -1:
            return render(request, 'iitr_drive/add_folder.html')
        else:
            return render(request, 'iitr_drive/folder.html', {'folderid': parent_id})
    return JsonResponse({ 'message': "Invalid Request" })


def lauda(request, file_id):
    file_obj = get_object_or_404(File, id=file_id)
    context = {
        'file_obj': file_obj,
    }
    return render(request, 'iitr_drive/view_shared_file.html', context)

def generate_qr_code(request, file_id):
    file_obj = get_object_or_404(File, id=file_id)
    file_url = request.build_absolute_uri(file_obj.file.url)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=1,
    )
    qr.add_data(file_url)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    qr_image.save(buffer, format="PNG")
    qr_image_data = buffer.getvalue()
    
    response = HttpResponse(qr_image_data, content_type="image/png")
    response['Content-Disposition'] = f'attachment; filename="{file_obj.filetitle}_qr.png"'

    return response

@login_required
def delete_file(request, file_id):
    try:
        file = File.objects.get(id=file_id)
        if file.folder.owner == request.user:
            file.delete()
            return JsonResponse({'success': True, 'message': 'File deleted successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Permission denied'})
    except File.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'File not found'})