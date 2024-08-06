from django.urls import path
from . import views

app_name = "admin_page_app"

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # # Course management
    path('courses/', views.course_list, name='course_list'),
    path('courses/register/', views.add_courses, name='add_courses'),
    path('courses/update/<int:course_id>/', views.update_course, name='update_course'),
    path('course/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    

    # # Instructor management
    path('instructors/', views.instructor_list, name='instructor_list'),


    # # Student management
    path('students/', views.student_list, name='student_list'), 
    path('students/details/<int:student_id>/', views.view_student_details, name='view_student_details'),

    # # Payment management
    path('payments/add/', views.add_payment, name='add_payment'),
    path('payments/update/<int:payment_id>/', views.update_payment, name='update_payment'),
    path('payments/delete/<int:payment_id>/', views.delete_payment, name='delete_payment'),
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/view/<int:payment_id>/', views.view_payment_student_details, name='view_payment_student_details'),

    # # Lesson management
    path('lessons/add/', views.add_lessons, name='add_lessons'),
    path('lessons/update/<int:lesson_id>/', views.update_lesson, name='update_lesson'),
    path('lessons/delete/<int:lesson_id>/', views.delete_lesson, name='delete_lesson'),
    path('lessons/', views.list_lessons, name='list_lessons'),
    path('courses/<int:course_id>/lessons/', views.view_course_lessons, name='view_course_lessons'),

    # # Reports
    # path('reports/enrollment/', views.enrollment_report, name='enrollment_report'),
    # path('reports/completion/', views.completion_report, name='completion_report'),
    # path('reports/financial/', views.financial_report, name='financial_report'),

    # # Event management
    # path('events/', views.event_list, name='event_list'), 
    # path('events/add/', views.add_event, name='add_event'),
    # path('events/update/<int:id>/', views.update_event, name='update_event'),
    # path('events/delete/<int:id>/', views.delete_event, name='delete_event'),

    # # Category management
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_categories, name='add_categories'),
    path('category/update/<int:category_id>/', views.update_category, name='update_category'),  # Correct parameter name
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('categories/<int:category_id>/courses/', views.view_category_courses, name='view_category_courses'),

    # # Quiz management
    # path('quizzes/', views.quiz_list, name='quiz_list'),
    # path('quizzes/add/', views.add_quiz, name='add_quiz'),
    # path('quizzes/update/<int:id>/', views.update_quiz, name='update_quiz'),
    # path('quizzes/delete/<int:id>/', views.delete_quiz, name='delete_quiz'),

    # # Certification management
    # path('certifications/', views.certification_list, name='certification_list'),
    # path('certifications/update/<int:id>/', views.update_certification, name='update_certification'),
    # path('certifications/issue/<int:id>/', views.issue_certification, name='issue_certification'),

    # # User roles and permissions management
    # path('users/', views.user_list, name='user_list'),
    # path('users/roles/', views.user_roles, name='user_roles'),
    # path('users/permissions/', views.user_permissions, name='user_permissions'),

    # admin mangamenter
    path('admin/view/', views.view_admins, name='view_admins'),

    # # System logs
    # path('logs/', views.system_logs, name='system_logs'),
]
