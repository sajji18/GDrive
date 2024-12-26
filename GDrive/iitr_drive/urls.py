from django.urls import path
from iitr_drive import views

urlpatterns = [
     path('folder_list/', views.folder_list, name='folder_list'),
     path('add_folder/', views.add_folder, name='add_folder'),
     path('view_shared_file/<int:file_id>/',views.lauda, name='view_shared_file'),
     path('folder/<int:folderid>/', 
          views.folder_detail, 
          name='folder'
          ),
     path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
     # path('folder/<int:parent_id>/add_child_folder/', 
     #      views.add_child_folder, 
     #      name='add_child_folder'
     #      ),
     # path('folder/<int:parent_id>/<int:child_id>/', 
     #      views.child_folder_view, 
     #      name='child_folder_view'
     #      ),
     path('generate_qr_code/<int:file_id>/', 
          views.generate_qr_code, 
          name='generate_qr_code'
          ),
]
