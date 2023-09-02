from django.shortcuts import render, redirect, get_object_or_404
from .forms import FolderForm
from .models import Folder, File
from django.urls import reverse
import qrcode
from io import BytesIO
from PIL import Image
from django.http import HttpResponse, JsonResponse

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


def generate_qr_code(request, file_id):
    # Get the file from your database or wherever it's stored
    # Replace this with your own logic to fetch the file
    file = File.objects.get(id=file_id)
    file_url = file.file.url

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(file_url)  # Assuming 'url' is the URL to the file
    qr.make(fit=True)

    # Create an image from the QR code
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Prepare the image for rendering in a template
    buffer = BytesIO()
    qr_image.save(buffer, format="PNG")
    qr_image_data = buffer.getvalue()

    return HttpResponse(qr_image_data, content_type="image/png")