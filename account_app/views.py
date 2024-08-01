from django.shortcuts import render
from .utils import execute_query, extract_user_data, hash_password
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid


# Create your views here.


# -----------------------------------------------------> 1) Start: Regiseration Management <-----------------------------------------------------

# 1.1) Add Student by Admin
def add_student_by_admin(request):
    if request.method == 'POST':
        data, errors = extract_user_data(request)
        if errors:
            return render(request, 'account_app/admin_student_register.html', {'errors': errors, 'data': data})
        
        if not data['password']:
            messages.error(request, 'Password is required.')
            return render(request, 'account_app/admin_student_register.html', {'data': data})
        
        if not data['email_address']:
            messages.error(request, 'Email address is required.')
            return render(request, 'account_app/admin_student_register.html', {'data': data})

        data['password'] = hash_password(data['password'])  # Hash the password
        query = """
            INSERT INTO students (first_name, middle_name, last_name, email_address, password, phone_number, gender, date_of_birth, address, major, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        params = [data['first_name'], data['middle_name'], data['last_name'], data['email_address'], data['password'], data['phone_number'], data['gender'], data['date_of_birth'], data['address'], data['major']]
        execute_query(query, params)
        messages.success(request, 'Student added successfully by admin!')
        return redirect('admin_page_app:student_list')

    return render(request, 'account_app/admin_student_register.html')

# 1.2) Add Student by User
def add_student_by_user(request):
    if request.method == 'POST':
        data, errors = extract_user_data(request)
        if errors:
            return render(request, 'account_app_partials/register_student_by_user.html', {'errors': errors, 'data': data})
        
        if not data['email_address']:
            messages.error(request, 'Email address is required.')
            return render(request, 'account_app_partials/register_student_by_user.html', {'data': data})

        if not data['password']:
            messages.error(request, 'Password is required.')
            return render(request, 'account_app_partials/register_student_by_user.html', {'data': data})

        data['password'] = hash_password(data['password'])  # Hash the password
        query = """
            INSERT INTO students (first_name, middle_name, last_name, email_address, password, phone_number, gender, date_of_birth, address, major, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        params = [data['first_name'], data['middle_name'], data['last_name'], data['email_address'], data['password'], data['phone_number'], data['gender'], data['date_of_birth'], data['address'], data['major']]
        execute_query(query, params)
        messages.success(request, 'Student registered successfully!')
        return redirect('home_page_app:home')

    return render(request, 'account_app_partials/register_student_by_user.html')


# 1.3) Add Student from Slider
def add_student_from_slider(request):
    if request.method == 'POST':
        data, errors = extract_user_data(request)
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'account_app/slider_student_register.html', {'errors': errors, 'data': data})
        
        if not data['email_address']:
            messages.error(request, 'Email address is required.')
            return render(request, 'account_app/slider_student_register.html', {'data': data})
        
        if not data['password']:
            messages.error(request, 'Password is required.')
            return render(request, 'account_app/slider_student_register.html', {'data': data})

        data['password'] = hash_password(data['password'])  # Hash the password
        query = """
            INSERT INTO students (first_name, middle_name, last_name, email_address, password, phone_number, gender, date_of_birth, address, major, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        params = [data['first_name'], data['middle_name'], data['last_name'], data['email_address'], data['password'], data['phone_number'], data['gender'], data['date_of_birth'], data['address'], data['major']]
        execute_query(query, params)
        messages.success(request, 'Student registered successfully!')
        return redirect('home_page_app:home')

    return render(request, 'account_app/slider_student_register.html')

# -----------------------------------------------------> End: Regiseration Management <-----------------------------------------------------

def delete_student(request, id):
    query = "DELETE FROM students WHERE id = %s"
    execute_query(query, [id])

    messages.success(request, 'Student deleted successfully!')
    return redirect('admin_page_app:student_list')



# -----------------------------------------------------> 2) Start: Login Management <-----------------------------------------------------

# 2.1) Login
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email_address')
        password = request.POST.get('password') 
        
        query = "SELECT * FROM students WHERE email_address = %s"
        student = execute_query(query, [email], fetchone=True)
        
        if student and check_password(password, student['password']):
            request.session['student_id'] = student['id']
            request.session['student_email'] = student['email_address']
            request.session['student_name'] = student['first_name']
            messages.success(request, 'Logged in successfully!')
            return redirect('home_page_app:student_dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('account_app:login')
    
    return render(request, 'account_app_partials/login_student.html')

# 2.2) Logout
def logout_view(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully!')
    return redirect('home_page_app:home')

# -----------------------------------------------------> End: Login Management <-----------------------------------------------------





# -----------------------------------------------------> 3) Start: Student Profile Management <-----------------------------------------------------


# 3.1) update_student_and_profile
def update_student_and_profile_by_user(request):
    student_id = request.session.get('student_id')
    if not student_id:
        messages.error(request, 'You need to log in to update your profile.')
        return redirect('home_page_app:login')

    if request.method == 'POST':
        data, errors = extract_user_data(request)
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'account_app/user_student_update.html', {'student': data})

        query = """
            UPDATE students SET first_name=%s, middle_name=%s, last_name=%s, phone_number=%s, gender=%s, date_of_birth=%s, address=%s, major=%s, created_at=NOW()
            WHERE id=%s
        """
        params = [data['first_name'], data['middle_name'], data['last_name'], data['phone_number'], data['gender'], data['date_of_birth'], data['address'], data['major'], student_id]
        execute_query(query, params)

        profile_data = {
            'bio': request.POST.get('bio'),
            'facebook': request.POST.get('facebook'),
            'twitter': request.POST.get('twitter'),
            'linkedIn': request.POST.get('linkedIn'),
            'github': request.POST.get('github'),
            'user_type': 'student',
            'user_id': student_id
        }

        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            profile_picture_path = os.path.join('profile_images', profile_picture.name)
            with open(os.path.join(settings.MEDIA_ROOT, profile_picture_path), 'wb+') as destination:
                for chunk in profile_picture.chunks():
                    destination.write(chunk)
            profile_data['profile_picture'] = profile_picture_path
        else:
            profile = execute_query("SELECT profile_picture FROM profiles WHERE user_id = %s AND user_type = 'student'", [student_id], fetchone=True)
            if profile:
                profile_data['profile_picture'] = profile['profile_picture']

        query = """
            UPDATE profiles SET bio=%s, facebook=%s, twitter=%s, linkedIn=%s, github=%s, profile_picture=%s, user_type=%s, user_id=%s, created_at=NOW()
            WHERE user_id=%s AND user_type='student'
        """
        params = [
            profile_data['bio'], profile_data['facebook'], profile_data['twitter'],
            profile_data['linkedIn'], profile_data['github'], profile_data.get('profile_picture'),
            profile_data['user_type'], profile_data['user_id'], student_id
        ]
        execute_query(query, params)
        messages.success(request, 'Student profile updated successfully!')
        return redirect('home_page_app:student_dashboard')

    student = execute_query("SELECT * FROM students WHERE id = %s", [student_id], fetchone=True)
    profile = execute_query("SELECT * FROM profiles WHERE user_id = %s AND user_type = 'student'", [student_id], fetchone=True)

    profile_picture_url = os.path.join(settings.MEDIA_URL, profile['profile_picture']).replace('\\', '/') if profile and profile.get('profile_picture') else None

    return render(request, 'account_app/user_student_update.html', {'student': student, 'profile': profile, 'profile_picture_url': profile_picture_url})


# 3.2) Upload Profile Picture
def upload_profile_picture(request):
    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        if not profile_picture:
            return JsonResponse({'error': 'No profile picture uploaded.'})

        student_id = request.session.get('student_id')
        if not student_id:
            return JsonResponse({'error': 'Student ID not found in session.'})

        profile_picture_path = os.path.join('profile_images', profile_picture.name)
        with open(os.path.join(settings.MEDIA_ROOT, profile_picture_path), 'wb+') as destination:
            for chunk in profile_picture.chunks():
                destination.write(chunk)

        profile_picture_url = os.path.join(settings.MEDIA_URL, profile_picture_path).replace('\\', '/')

        existing_profile = execute_query(
            "SELECT COUNT(*) as count FROM profiles WHERE user_id = %s AND user_type = 'student'", [student_id], fetchone=True
        )

        if existing_profile and existing_profile['count'] > 0:
            query = """
                UPDATE profiles 
                SET profile_picture=%s, created_at=NOW()
                WHERE user_id=%s AND user_type='student'
            """
            params = [profile_picture_path, student_id]
        else:
            query = """
                INSERT INTO profiles (profile_picture, user_type, user_id, created_at) 
                VALUES (%s, 'student', %s, NOW())
            """
            params = [profile_picture_path, student_id]

        execute_query(query, params)
        return JsonResponse({'profile_picture_url': profile_picture_url})

    return JsonResponse({'error': 'Invalid request method.'})



def update_student_and_profile_by_admin(request, student_id):
    if request.method == 'POST':
        data, errors = extract_user_data(request)

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('account_app:update_student_and_profile_by_admin', student_id=student_id)

        update_student_query = """
            UPDATE students
            SET first_name = %s, middle_name = %s, last_name = %s, phone_number = %s, gender = %s, date_of_birth = %s, address = %s, major = %s
            WHERE id = %s
        """
        student_params = [data['first_name'], data['middle_name'], data['last_name'], data['phone_number'], data['gender'], data['date_of_birth'], data['address'], data['major'], student_id]
        execute_query(update_student_query, student_params)

        update_profile_query = """
            UPDATE profiles
            SET bio = %s, facebook = %s, twitter = %s, linkedIn = %s, github = %s, profile_picture = %s
            WHERE user_id = %s AND user_type = 'student'
        """
        profile_params = [data['bio'], data['facebook'], data['twitter'], data['linkedIn'], data['github'], data['profile_picture'], student_id]
        execute_query(update_profile_query, profile_params)
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('account_app:student_list')

    student_query = "SELECT * FROM students WHERE id = %s"
    student = execute_query(student_query, [student_id], fetchone=True)

    profile_query = "SELECT * FROM profiles WHERE user_id = %s AND user_type = 'student'"
    profile = execute_query(profile_query, [student_id], fetchone=True)

    return render(request, 'account_app/admin_student_update.html', {'student': student, 'profile': profile})
# -----------------------------------------------------> End: Student Profile Management <-----------------------------------------------------