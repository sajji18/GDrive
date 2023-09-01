from django.urls import path
from iitr_drive import views

urlpatterns = [
    path('folder_list/', views.folder_list, name='folder_list'),
    path('add_folder/', views.add_folder, name='add_folder'),
    path('folder/<int:folderid>/', views.folder_detail, name='folder')
]
