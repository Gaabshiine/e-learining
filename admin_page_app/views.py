from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from account_app.models import Student # Create your views here.
from .utils import execute_query




def dashboard(request): 
    return render(request, 'admin_page_app/admin_dashboard.html')


def student_list(request):
    students = execute_query("SELECT * FROM students", fetchall=True)
    return render(request, 'admin_page_app/view_students.html', {'students': students}) 



