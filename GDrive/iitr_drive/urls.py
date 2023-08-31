from django.urls import path
from iitr_drive import views

urlpatterns = [
    path('folders/', views.folder, name='folders'),
    path('add_folder/', views.add_folder, name='add_folder'),
]
