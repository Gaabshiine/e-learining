from django.shortcuts import render
from django.shortcuts import render, redirect
from .utils import execute_query
from django.http import JsonResponse
from django.conf import settings
import os
from django.urls import reverse


#--------------------------------- 1) Start: Admin Dashboard---------------------------------#
# 1.1) Admin Dashboard
def dashboard(request):
    """
    View for the admin dashboard. Retrieves admin profile and passes it to the template.
    """
    admin_profile = None

    # Check if the admin_id is set in the session
    if 'admin_id' in request.session:
        # Fetch admin profile from the database
        query = "SELECT * FROM admins WHERE id = %s"
        admin_profile = execute_query(query, [request.session['admin_id']], fetchone=True)

    if not admin_profile:
        # If no admin is found, redirect to the login page
        return redirect(reverse('account_app:admin_login'))

    # Fetch or create the admin's profile
    profile_query = "SELECT * FROM profiles WHERE user_id = %s AND user_type = 'admin'"
    profile = execute_query(profile_query, [admin_profile['id']], fetchone=True)


    # Construct the profile picture URL
    profile_picture_url = os.path.join(settings.MEDIA_URL, profile['profile_picture']).replace('\\', '/') if profile and profile.get('profile_picture') else None

    # Add context for the admin profile
    context = {
        'admin_user': admin_profile,
        'profile_picture_url': profile_picture_url,
    }

    return render(request, 'admin_page_app/admin_dashboard.html', context)

#--------------------------------- End: Admin Dashboard---------------------------------#


#--------------------------------- 2) Start: views and details all about the system ---------------------------------#

# 2.1) View all students
def student_list(request):
    students = execute_query("SELECT * FROM students", fetchall=True)
    return render(request, 'admin_page_app/view_students.html', {'students': students}) 


# 2.2) View all instructors
def instructor_list(request):
    instructors = execute_query("SELECT * FROM instructors", fetchall=True)
    return render(request, 'admin_page_app/view_instructors.html', {'instructors': instructors}) 

# 2.3) View all admins
def view_admins(request):
    # Query to fetch all admins
    query = "SELECT * FROM admins ORDER BY created_at DESC"
    admins = execute_query(query, fetchall=True)

    # Render the admins list page
    return render(request, 'admin_page_app/view_admins.html', {'admins': admins})



"""
Objective:
We aim to allow students to request activation for their enrolled courses, which the admin can later approve or deny. 
The button display will vary depending on the activation request status.

Approach:
We'll use the ActivationRequest model to track activation requests and their statuses. 
Each course enrollment will have an associated activation request, which can be in one of three states: 
pending, approved, or rejected.
"""
def view_student_details(request, student_id):
    # Fetch student data
    student_query = "SELECT * FROM students WHERE id = %s"
    student = execute_query(student_query, [student_id], fetchone=True)

    # Ensure the student exists
    if not student:
        return JsonResponse({'success': False, 'error': 'Student not found.'}, status=404)

    # Fetch student profile data
    profile_query = "SELECT * FROM profiles WHERE user_id = %s AND user_type = 'student'"
    profile = execute_query(profile_query, [student_id], fetchone=True)

    # Fetch enrolled courses
    enrolled_courses_query = """
        SELECT e.id AS enrollment_id, c.id AS course_id, c.name AS course_name, cat.name AS category_name
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        JOIN categories cat ON c.category_id = cat.id
        WHERE e.student_id = %s
    """
    enrolled_courses = execute_query(enrolled_courses_query, [student_id], fetchall=True)

    # Fetch activation requests to check their status
    activation_requests_query = """
        SELECT ar.id AS request_id, ar.status, ar.course_id
        FROM activation_requests ar
        WHERE ar.student_id = %s
    """
    activation_requests = execute_query(activation_requests_query, [student_id], fetchall=True)

    # Create a dictionary to map course_id to request status
    activation_request_status = {request['course_id']: request['status'] for request in activation_requests}

    # Add activation status to each enrolled course
    for course in enrolled_courses:
        course['activation_status'] = activation_request_status.get(course['course_id'], 'none')

    profile_picture_url = os.path.join(settings.MEDIA_URL, profile['profile_picture']).replace('\\', '/') if profile and profile.get('profile_picture') else None

    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment_id')

        # Fetch the course ID for the enrollment
        course_query = "SELECT course_id FROM enrollments WHERE id = %s"
        course = execute_query(course_query, [enrollment_id], fetchone=True)

        if not course:
            return JsonResponse({'success': False, 'error': 'Enrollment not found.'}, status=404)

        course_id = course['course_id']

        # Check if an activation request is already pending or approved
        existing_request_query = """
            SELECT * FROM activation_requests WHERE student_id = %s AND course_id = %s AND status IN ('pending', 'approved')
        """
        existing_request = execute_query(existing_request_query, [student_id, course_id], fetchone=True)

        if existing_request:
            return JsonResponse({'success': False, 'error': 'An activation request is already pending or approved for this course.'}, status=400)

        # Create a new activation request
        create_activation_request_query = """
            INSERT INTO activation_requests (student_id, course_id, request_date, status)
            VALUES (%s, %s, NOW(), 'pending')
        """
        execute_query(create_activation_request_query, [student_id, course_id])
        return JsonResponse({'success': True, 'message': 'Activation request submitted successfully.'}, status=200)

    return render(request, 'admin_page_app/admin_student_details.html', {
        'student': student,
        'profile': profile,
        'enrolled_courses': enrolled_courses,
        'profile_picture_url': profile_picture_url,
    })
#--------------------------------- End: views and details all about the system ---------------------------------#






