from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from account_app.models import Student # Create your views here.
from .utils import execute_query




def dashboard(request):
    return render(request, 'admin_page_app/admin_dashboard.html')


def student_list(request):
    students = execute_query("SELECT * FROM students", fetchall=True)
    return render(request, 'admin_page_app/view_students.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        email_address = request.POST.get('type_email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')
        major = request.POST.get('major')

        query = """
            INSERT INTO students (first_name, middle_name, last_name, email_address, password, phone_number, gender, date_of_birth, address, major, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        params = [first_name, middle_name, last_name, email_address, password, phone_number, gender, date_of_birth, address, major]
        execute_query(query, params)

        messages.success(request, 'Student added successfully!')
        return redirect('admin_page_app:student_list')
    return render(request, 'admin_page_app/admin_student_register.html')

def update_student(request, id):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        email_address = request.POST.get('type_email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')
        major = request.POST.get('major')

        query = """
            UPDATE students
            SET first_name = %s, middle_name = %s, last_name = %s, email_address = %s, password = %s, phone_number = %s, gender = %s, date_of_birth = %s, address = %s, major = %s
            WHERE id = %s
        """
        params = [first_name, middle_name, last_name, email_address, password, phone_number, gender, date_of_birth, address, major, id]
        execute_query(query, params)

        messages.success(request, 'Student updated successfully!')
        return redirect('admin_page_app:student_list')
    else:
        query = "SELECT * FROM students WHERE id = %s"
        student = execute_query(query, [id], fetchone=True)
        return render(request, 'admin_page_app/admin_student_update.html', {'student': student})

def delete_student(request, id):
    query = "DELETE FROM students WHERE id = %s"
    execute_query(query, [id])

    messages.success(request, 'Student deleted successfully!')
    return redirect('admin_page_app:student_list')