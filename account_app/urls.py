from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "account_app"

urlpatterns = [
    # # Student management
    path('login/', views.login_view, name='login'),
    path('students/add/by_admin/', views.add_student_by_admin, name='add_student_by_admin'),
    path('students/add/by_user/', views.add_student_by_user, name='add_student_by_user'),
    path('students/add/from_slider/', views.add_student_from_slider, name='add_student_from_slider'),
    path('students/update/by_user/', views.update_student_and_profile_by_user, name='update_student_and_profile_by_user'),
    path('students/update/by_admin/<int:student_id>/', views.update_student_and_profile_by_admin, name='update_student_and_profile_by_admin'),
    path('students/delete/<int:id>/', views.delete_student, name='delete_student'),
    path('upload_profile_picture/', views.upload_profile_picture, name='upload_profile_picture'),

     

    

    # admin mangamenter
    # path('admins/', views.admin_list, name='admin_list'),
    # path('admins/add/', views.add_admin, name='add_admin'),

]

