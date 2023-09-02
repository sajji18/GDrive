from django.shortcuts import render, redirect, get_object_or_404
from .forms import FolderForm
from django.contrib.auth.decorators import login_required
from .models import Folder, File
from django.urls import reverse
import qrcode
from io import BytesIO
from PIL import Image
from django.http import HttpResponse, JsonResponse

@login_required
def folder_list(request):
    current_user = request.user
    folders = Folder.objects.filter(owner=current_user, linked_in=-1)

    context = {
        'folders': folders,
        'parent_id': -1
    }
    return render(request, 'iitr_drive/folder_list.html', context)


def folder_detail(request, folderid):
    if request.user.is_authenticated:
        folder_user = get_object_or_404(Folder, id=folderid)
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


from django.http import HttpResponse
import qrcode
from io import BytesIO

def generate_qr_code(request, file_id):
    # Fetch file from db
    file = File.objects.get(id=file_id)
    file_url = file.file.url

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=5,
    )
    qr.add_data(file_url)
    qr.make(fit=True)

    # Create an image from the QR code
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Prepare the image for rendering in a template
    buffer = BytesIO()
    qr_image.save(buffer, format="PNG")
    qr_image_data = buffer.getvalue()

    # Set the response content type to image/png
    response = HttpResponse(content_type="image/png")
    response.write(qr_image_data)

    return response
