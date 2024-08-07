from django.shortcuts import render
from django.shortcuts import render, redirect
from .utils import execute_query, BunnyCDNStorage
from django.http import JsonResponse
from django.conf import settings
import os
from django.urls import reverse
from datetime import datetime
from django.utils.dateparse import parse_date
from django.utils import timezone
from datetime import timedelta



#--------------------------------- 1) Start: Admin Dashboard---------------------------------#
# 1.1) Admin Dashboard
def get_percentage_change(current, previous):
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

def dashboard(request):
    # Fetching data for dashboard
    # Total counts
    total_students_query = "SELECT COUNT(*) AS total FROM students"
    total_instructors_query = "SELECT COUNT(*) AS total FROM instructors"
    total_courses_query = "SELECT COUNT(*) AS total FROM courses"
    total_enrollments_query = "SELECT COUNT(*) AS total FROM enrollments"
    total_revenue_query = "SELECT SUM(total_amount) AS total FROM payments"

    # Activation requests
    pending_activation_requests_query = "SELECT COUNT(*) AS total FROM activation_requests WHERE status = 'pending'"
    approved_activation_requests_query = "SELECT COUNT(*) AS total FROM activation_requests WHERE status = 'approved'"

    # Get current and previous month data
    today = datetime.today()
    first_day_of_current_month = today.replace(day=1)
    first_day_of_previous_month = (first_day_of_current_month - timedelta(days=1)).replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)

    current_month_payments_query = """
        SELECT SUM(total_amount) AS total FROM payments
        WHERE payment_date >= %s AND payment_date < %s
    """
    previous_month_payments_query = """
        SELECT SUM(total_amount) AS total FROM payments
        WHERE payment_date >= %s AND payment_date <= %s
    """

    # Execute queries
    total_students = execute_query(total_students_query, [], fetchone=True)['total']
    total_instructors = execute_query(total_instructors_query, [], fetchone=True)['total']
    total_courses = execute_query(total_courses_query, [], fetchone=True)['total']
    total_enrollments = execute_query(total_enrollments_query, [], fetchone=True)['total']
    total_revenue = execute_query(total_revenue_query, [], fetchone=True)['total'] or 0.0

    pending_activation_requests = execute_query(pending_activation_requests_query, [], fetchone=True)['total']
    approved_activation_requests = execute_query(approved_activation_requests_query, [], fetchone=True)['total']

    current_month_revenue = execute_query(current_month_payments_query, [first_day_of_current_month, today], fetchone=True)['total'] or 0.0
    previous_month_revenue = execute_query(previous_month_payments_query, [first_day_of_previous_month, last_day_of_previous_month], fetchone=True)['total'] or 0.0

    # Calculate percentage changes
    student_percentage_change = get_percentage_change(total_students, total_students - pending_activation_requests)
    instructor_percentage_change = get_percentage_change(total_instructors, total_instructors - approved_activation_requests)
    course_percentage_change = get_percentage_change(total_courses, total_courses)  # Assuming no previous month data
    enrollment_percentage_change = get_percentage_change(total_enrollments, total_enrollments - pending_activation_requests)
    revenue_percentage_change = get_percentage_change(current_month_revenue, previous_month_revenue)

    context = {
        'dashboard_total_students': total_students,
        'student_percentage_change': student_percentage_change,
        'dashboard_total_instructors': total_instructors,
        'instructor_percentage_change': instructor_percentage_change,
        'dashboard_total_courses': total_courses,
        'course_percentage_change': course_percentage_change,
        'dashboard_total_enrollments': total_enrollments,
        'enrollment_percentage_change': enrollment_percentage_change,
        'dashboard_total_revenue': total_revenue,
        'revenue_percentage_change': revenue_percentage_change,
        'dashboard_pending_activation_requests': pending_activation_requests,
        'dashboard_approved_activation_requests': approved_activation_requests,
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


# 2.4) View all categories
def category_list(request):
    categories = execute_query("SELECT * FROM categories", [], fetchall=True)  # Fetch categories from DB
    return render(request, 'admin_page_app/view_categories.html', {
        'categories': categories,
        'MEDIA_URL': settings.MEDIA_URL
    })


# 2.5) View all courses
def course_list(request):
    query = """
        SELECT c.id, c.name, c.description, c.start_date, c.end_date, c.course_amount,
               c.image, cat.name as category_name, i.first_name as instructor_first_name, i.last_name as instructor_last_name
        FROM courses c
        JOIN categories cat ON c.category_id = cat.id
        JOIN instructors i ON c.instructor_id = i.id
    """
    courses = execute_query(query, fetchall=True)
    return render(request, 'admin_page_app/view_courses.html', {'courses': courses})


# 2.6) View all payments
def payment_list(request):
    # Updated SQL query reflecting an enrollment table
    query = """
        SELECT payments.id, payments.expected_course_amount, payments.discount, 
               payments.total_amount, payments.payment_date, 
               students.first_name, students.middle_name, students.last_name
        FROM payments
        JOIN courses ON payments.course_id = courses.id
        JOIN enrollments ON enrollments.course_id = courses.id
        JOIN students ON students.id = enrollments.student_id
    """
    payments = execute_query(query, [], fetchall=True)
    return render(request, 'admin_page_app/view_payments.html', {
        'payments': payments,
        'MEDIA_URL': settings.MEDIA_URL
    })

# 2.7) View all lessons
# admin_page_app/views.py

def list_lessons(request):
    # Fetch all lessons with their course and category information
    lessons = execute_query("""
        SELECT l.id, l.title, l.content, l.video_url, l.created_at, 
               c.name AS course_name, cat.name AS category_name
        FROM lessons l
        JOIN courses c ON l.course_id = c.id
        JOIN categories cat ON c.category_id = cat.id
    """, [], fetchall=True)

    return render(request, 'admin_page_app/view_lessons.html', {'lessons': lessons})


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


def view_payment_student_details(request, payment_id):
    query = """
        SELECT payments.id, payments.expected_course_amount, payments.discount, 
               payments.total_amount, payments.payment_date, 
               students.first_name, students.middle_name, students.last_name,
               courses.name as course_name
        FROM payments
        JOIN courses ON payments.course_id = courses.id
        JOIN students ON payments.student_id = students.id
        WHERE payments.id = %s
    """
    payment_details = execute_query(query, [payment_id], fetchone=True)
    return render(request, 'admin_page_app/view_payment_student_details.html', {
        'payment_details': payment_details,
        'MEDIA_URL': settings.MEDIA_URL
    })

def view_category_courses(request, category_id):
    # Fetch the specific category
    category = execute_query("SELECT * FROM categories WHERE id = %s", [category_id], fetchone=True)

    # Fetch courses associated with the category, including instructor's name
    courses = execute_query("""
        SELECT c.id, c.name, c.description, c.start_date, c.end_date, 
               c.course_amount, c.image, i.first_name, i.last_name
        FROM courses c
        JOIN instructors i ON c.instructor_id = i.id
        WHERE c.category_id = %s
    """, [category_id], fetchall=True)

    if not category:
        return render(request, 'admin_page_app/category_not_found.html')  # Render a template for category not found

    return render(request, 'admin_page_app/view_category_courses.html', {
        'category': category,
        'courses': courses,
        'MEDIA_URL': settings.MEDIA_URL
    })

def view_course_lessons(request, course_id):
    # Fetch the course details using a raw SQL query
    course = execute_query("SELECT * FROM courses WHERE id = %s", [course_id], fetchone=True)

    if not course:
        # Return a 404 error if the course does not exist
        return render(request, '404.html', status=404)

    # Fetch lessons related to the course using a raw SQL query
    lessons = execute_query("""
        SELECT l.id, l.title, l.content, l.video_url, l.created_at
        FROM lessons l
        WHERE l.course_id = %s
    """, [course_id], fetchall=True)

    context = {
        'course': course,
        'lessons': lessons
    }

    return render(request, 'admin_page_app/view_course_lessons.html', context)


#--------------------------------- End: views and details all about the system ---------------------------------#



#--------------------------------- 3) Start: Add views record to the system ---------------------------------#

# 3.1) Add a new category
def add_categories(request):
    if request.method == 'POST':
        number_of_categories = int(request.POST.get('number_of_categories', '0'))
        errors = {}
        success = True

        for i in range(number_of_categories):
            name = request.POST.get(f'name_{i}', '').strip()
            description = request.POST.get(f'description_{i}', '').strip()
            image = request.FILES.get(f'image_{i}')

            # Validate inputs
            if not name:
                errors[f'name_{i}'] = 'Name is required.'
                success = False
            if not description:
                errors[f'description_{i}'] = 'Description is required.'
                success = False

            # Check if the category already exists
            query = "SELECT COUNT(*) FROM categories WHERE name = %s"
            if execute_query(query, [name], fetchone=True)['COUNT(*)'] > 0:
                errors[f'name_{i}'] = 'Category already exists.'
                success = False

            # Handle image upload
            image_path = None
            if image:
                image_directory = os.path.join(settings.MEDIA_ROOT, 'category_images')
                os.makedirs(image_directory, exist_ok=True)
                image_path = os.path.join(image_directory, image.name)

                with open(image_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

                image_path = f'category_images/{image.name}'

            # Insert the new category into the database
            if success:
                query = """
                    INSERT INTO categories (name, description, image, created_at)
                    VALUES (%s, %s, %s, NOW())
                """
                params = [name, description, image_path]
                execute_query(query, params)

        if success:
            return JsonResponse({
                'success': True,
                'message': 'Categories added successfully!',
                'redirect_url': reverse('admin_page_app:category_list')
            })
        else:
            return JsonResponse({'success': False, 'errors': errors})

    return render(request, 'admin_page_app/admin_category_register.html')

# 3.2) Add a new course
def add_courses(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        number_of_courses = int(request.POST.get('number_of_courses', 0))
        category_id = request.POST.get('category')
        
        errors = {}

        # Validate inputs
        if number_of_courses <= 0:
            errors['number_of_courses'] = 'Number of courses must be greater than zero.'
        
        if not category_id:
            errors['category'] = 'Category is required.'

        courses = []
        for i in range(number_of_courses):
            name = request.POST.get(f'name_{i}', '').strip()
            description = request.POST.get(f'description_{i}', '').strip()
            start_date = request.POST.get(f'start_date_{i}', '')
            end_date = request.POST.get(f'end_date_{i}', '')
            course_amount = request.POST.get(f'course_amount_{i}', '')
            instructor_id = request.POST.get(f'instructor_{i}', '')
            image = request.FILES.get(f'image_{i}')

            # Validate individual course inputs
            if not name:
                errors[f'name_{i}'] = f'Name for course {i+1} is required.'
            
            if not description:
                errors[f'description_{i}'] = f'Description for course {i+1} is required.'
            
            if not start_date:
                errors[f'start_date_{i}'] = f'Start date for course {i+1} is required.'
            
            if not course_amount:
                errors[f'course_amount_{i}'] = f'Course amount for course {i+1} is required.'

            if not instructor_id:
                errors[f'instructor_{i}'] = f'Instructor for course {i+1} is required.'
            
            # Validate start and end dates
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                if end_date:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                errors[f'start_date_{i}'] = f'Invalid date format for course {i+1}.'

            # Handle image upload
            image_path = None
            if image:
                image_directory = os.path.join(settings.MEDIA_ROOT, 'course_images')
                os.makedirs(image_directory, exist_ok=True)
                image_path = os.path.join(image_directory, image.name)

                with open(image_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

                image_path = f'course_images/{image.name}'
            
            courses.append({
                'name': name,
                'description': description,
                'start_date': start_date,
                'end_date': end_date,
                'course_amount': course_amount,
                'category_id': category_id,
                'instructor_id': instructor_id,
                'image': image_path,
            })
        
        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        
        # Insert courses into the database
        for course in courses:
            query = """
                INSERT INTO courses (name, description, start_date, end_date, course_amount, category_id, instructor_id, image, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """
            params = [
                course['name'], course['description'], course['start_date'],
                course['end_date'], course['course_amount'], course['category_id'],
                course['instructor_id'], course['image']
            ]
            execute_query(query, params)
        
        return JsonResponse({
            'success': True,
            'message': 'Courses added successfully!',
            'redirect_url': reverse('admin_page_app:course_list')
        })

    categories = execute_query("SELECT id, name FROM categories", [], fetchall=True)
    instructors = execute_query("SELECT id, first_name, last_name FROM instructors", [], fetchall=True)
    return render(request, 'admin_page_app/admin_course_register.html', {
        'categories': categories,
        'instructors': instructors
    })


# 3.3) Add a new payment
def add_payment(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        course_id = request.POST.get('course')
        expected_course_amount = request.POST.get('expected_course_amount', '0.00')
        discount = request.POST.get('discount', '0.00')
        payment_date = request.POST.get('payment_date')

        # Calculate total amount after discount
        try:
            expected_course_amount = float(expected_course_amount)
            discount = float(discount)
            total_amount = expected_course_amount - (expected_course_amount * (discount / 100))
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid amount or discount format.'})

        # Validate inputs
        errors = {}
        if not student_id:
            errors['student'] = 'Student is required.'
        if not course_id:
            errors['course'] = 'Course is required.'
        if not payment_date:
            errors['payment_date'] = 'Payment date is required.'

        if errors:
            return JsonResponse({'success': False, 'errors': errors})

        # Check if the student is enrolled in the course
        enrollment_exists = execute_query(
            "SELECT COUNT(*) as count FROM enrollments WHERE student_id = %s AND course_id = %s",
            [student_id, course_id],
            fetchone=True
        )
        if not enrollment_exists or enrollment_exists['count'] == 0:
            return JsonResponse({'success': False, 'error': 'The student is not enrolled in this course.'})

        # Insert the payment into the database
        query = """
            INSERT INTO payments (student_id, course_id, expected_course_amount, discount, total_amount, payment_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = [student_id, course_id, expected_course_amount, discount, total_amount, payment_date]
        execute_query(query, params)

        return JsonResponse({'success': True, 'redirect_url': reverse('admin_page_app:payment_list')})

    # Fetch students who are enrolled in at least one course
    students = execute_query("""
        SELECT DISTINCT students.id, students.first_name, students.last_name
        FROM students
        INNER JOIN enrollments ON students.id = enrollments.student_id
    """, [], fetchall=True)

    # Fetch available courses
    courses = execute_query("SELECT id, name FROM courses", [], fetchall=True)

    return render(request, 'admin_page_app/admin_payment_register.html', {'students': students, 'courses': courses})

# 3.4) Add a new lesson
def add_lessons(request):
    # Fetch courses along with their category names
    courses = execute_query("""
        SELECT c.id, c.name AS course_name, cat.name AS category_name
        FROM courses c
        JOIN categories cat ON c.category_id = cat.id
    """, [], fetchall=True)

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        number_of_lessons = int(request.POST.get('number_of_lessons', '0'))
        course_id = request.POST.get('course', '').strip()
        errors = {}
        success = True

        # Validate inputs
        if not course_id:
            errors['course'] = 'Course is required.'
            success = False

        for i in range(number_of_lessons):
            title = request.POST.get(f'title_{i}', '').strip()
            content = request.POST.get(f'content_{i}', '').strip()
            video_file = request.FILES.get(f'video_file_{i}')

            if not title:
                errors[f'title_{i}'] = 'Title is required.'
                success = False
            if not content:
                errors[f'content_{i}'] = 'Content is required.'
                success = False

            video_url = None
            if video_file:
                try:
                    # Upload video to BunnyCDN
                    bunny_client = BunnyCDNStorage()

                    # Find the course and its category for the storage path
                    course = next((c for c in courses if str(c['id']) == course_id), None)
                    if course:
                        category_name = course['category_name'].replace(" ", "_")
                        course_name = course['course_name'].replace(" ", "_")
                        storage_path = f"{settings.BUNNY_CDN_STORAGE_ZONE_NAME}/{category_name}/{course_name}/"

                        video_url = bunny_client.upload_file(storage_path, video_file, video_file.name)
                except Exception as e:
                    errors[f'video_file_{i}'] = f'Error uploading video: {str(e)}'
                    success = False

            if success:
                # Insert lesson into the database
                query = """
                    INSERT INTO lessons (title, content, course_id, video_url, created_at)
                    VALUES (%s, %s, %s, %s, NOW())
                """
                params = [title, content, course_id, video_url]
                execute_query(query, params)

        if success:
            return JsonResponse({
                'success': True,
                'message': 'Lessons added successfully!',
                'redirect_url': reverse('admin_page_app:list_lessons')
            })
        else:
            return JsonResponse({'success': False, 'errors': errors})

    return render(request, 'admin_page_app/admin_lesson_register.html', {'courses': courses})

#--------------------------------- End: Add views record to the system ---------------------------------#



#--------------------------------- 4) Start: update views record from the system ---------------------------------#

# 4.1) Update a category
def update_category(request, category_id):
    category = execute_query("SELECT * FROM categories WHERE id = %s", [category_id], fetchone=True)

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        # Validate inputs
        errors = {}
        if not name:
            errors['name'] = 'Name is required.'
        if not description:
            errors['description'] = 'Description is required.'

        # Return errors if any
        if errors:
            return JsonResponse({'success': False, 'errors': errors})

        # Handle image upload
        image_path = category['image']  # Use existing image path if not updated
        if image:
            image_directory = os.path.join(settings.MEDIA_ROOT, 'category_images')
            os.makedirs(image_directory, exist_ok=True)
            image_path = os.path.join(image_directory, image.name)
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            image_path = f'category_images/{image.name}'

        # Update category in the database
        update_query = """
            UPDATE categories SET name = %s, description = %s, image = %s WHERE id = %s
        """
        execute_query(update_query, [name, description, image_path, category_id])

        return JsonResponse({'success': True, 'redirect_url': reverse('admin_page_app:category_list')})

    return render(request, 'admin_page_app/admin_category_update.html', {'category': category, 'MEDIA_URL': settings.MEDIA_URL})

# 4.2) Update a course
def update_course(request, course_id):
    # Fetch course details from the database
    course = execute_query("SELECT * FROM courses WHERE id = %s", [course_id], fetchone=True)
    if not course:
        return JsonResponse({'success': False, 'error': 'Course not found.'})
    
    # Format the date fields
    if course['start_date']:
        course['start_date'] = course['start_date'].strftime('%Y-%m-%d')
    if course['end_date']:
        course['end_date'] = course['end_date'].strftime('%Y-%m-%d')

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        start_date = request.POST.get('start_date', '').strip()  # Fetch the start date from the form
        end_date = request.POST.get('end_date', '').strip()  # Fetch the end date from the form
        course_amount = request.POST.get('course_amount', '').strip()
        category_id = request.POST.get('category', '').strip()
        instructor_id = request.POST.get('instructor', '').strip()
        image = request.FILES.get('image')

        # Validate inputs
        errors = {}
        if not name:
            errors['name'] = 'Course name is required.'
        if not description:
            errors['description'] = 'Description is required.'
        if not start_date:
            errors['start_date'] = 'Start date is required.'
        if not course_amount:
            errors['course_amount'] = 'Course amount is required.'
        if not category_id:
            errors['category'] = 'Category is required.'
        if not instructor_id:
            errors['instructor'] = 'Instructor is required.'

        # Return errors if any
        if errors:
            return JsonResponse({'success': False, 'errors': errors})

        # Handle image upload
        image_path = course['image']  # Use existing image path if not updated
        if image:
            image_directory = os.path.join(settings.MEDIA_ROOT, 'course_images')
            os.makedirs(image_directory, exist_ok=True)
            image_path = os.path.join(image_directory, image.name)
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            image_path = f'course_images/{image.name}'

        # Ensure the start_date and end_date are in the correct format for the database
        try:
            formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
            formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid date format. Please use YYYY-MM-DD.'})

        # Update course in the database
        update_query = """
            UPDATE courses SET name = %s, description = %s, start_date = %s, end_date = %s, course_amount = %s, category_id = %s, instructor_id = %s, image = %s
            WHERE id = %s
        """
        params = [name, description, formatted_start_date, formatted_end_date, course_amount, category_id, instructor_id, image_path, course_id]
        try:
            execute_query(update_query, params)
            return JsonResponse({'success': True, 'redirect_url': reverse('admin_page_app:course_list')})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'An error occurred while updating the course. {str(e)}'})

    # If not a POST request, render the course update form
    categories = execute_query("SELECT * FROM categories", [], fetchall=True)
    instructors = execute_query("SELECT * FROM instructors", [], fetchall=True)
    return render(request, 'admin_page_app/admin_course_update.html', {
        'course': course,
        'categories': categories,
        'instructors': instructors,
        'MEDIA_URL': settings.MEDIA_URL
    })

# 4.3) Payment update
def update_payment(request, payment_id):
    payment = execute_query("SELECT * FROM payments WHERE id = %s", [payment_id], fetchone=True)
    if not payment:
        return JsonResponse({'success': False, 'error': 'Payment not found.'})

    if request.method == 'POST':
        student_id = request.POST.get('student')
        course_id = request.POST.get('course')
        expected_course_amount = request.POST.get('expected_course_amount', '0.00')
        discount = request.POST.get('discount', '0.00')
        payment_date = request.POST.get('payment_date')

        # Calculate total amount after discount
        try:
            expected_course_amount = float(expected_course_amount)
            discount = float(discount)
            total_amount = expected_course_amount - (expected_course_amount * (discount / 100))
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid amount or discount format.'})

        # Validate inputs
        errors = {}
        if not student_id:
            errors['student'] = 'Student is required.'
        if not course_id:
            errors['course'] = 'Course is required.'
        if not payment_date:
            errors['payment_date'] = 'Payment date is required.'

        if errors:
            return JsonResponse({'success': False, 'errors': errors})

        # Check if the student is enrolled in the course
        enrollment_exists = execute_query(
            "SELECT COUNT(*) as count FROM enrollments WHERE student_id = %s AND course_id = %s",
            [student_id, course_id],
            fetchone=True
        )
        if not enrollment_exists or enrollment_exists['count'] == 0:
            return JsonResponse({'success': False, 'error': 'The student is not enrolled in this course.'})

        # Update the payment in the database
        query = """
            UPDATE payments
            SET student_id = %s, course_id = %s, expected_course_amount = %s, discount = %s, total_amount = %s, payment_date = %s
            WHERE id = %s
        """
        params = [student_id, course_id, expected_course_amount, discount, total_amount, payment_date, payment_id]
        execute_query(query, params)

        return JsonResponse({'success': True, 'redirect_url': reverse('admin_page_app:payment_list')})

    # Fetch the payment details for editing
    students = execute_query("""
        SELECT DISTINCT students.id, students.first_name, students.last_name
        FROM students
        INNER JOIN enrollments ON students.id = enrollments.student_id
    """, [], fetchall=True)

    courses = execute_query("SELECT id, name FROM courses", [], fetchall=True)

    return render(request, 'admin_page_app/admin_payment_update.html', {
        'payment': payment,
        'students': students,
        'courses': courses
    })

# 4.4) Update a lesson
def update_lesson(request, lesson_id):
    lesson = execute_query("SELECT * FROM lessons WHERE id = %s", [lesson_id], fetchone=True)
    courses = execute_query("""
        SELECT c.id, c.name AS course_name, cat.name AS category_name
        FROM courses c
        JOIN categories cat ON c.category_id = cat.id
    """, [], fetchall=True)

    if not lesson:
        return JsonResponse({'success': False, 'error': 'Lesson not found.'})

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        course_id = request.POST.get('course', '').strip()
        video_file = request.FILES.get('video_file')

        # Validate inputs
        errors = {}
        if not title:
            errors['title'] = 'Title is required.'
        if not content:
            errors['content'] = 'Content is required.'
        if not course_id:
            errors['course'] = 'Course is required.'

        if errors:
            return JsonResponse({'success': False, 'errors': errors})

        # Handle video update
        video_url = lesson['video_url']
        if video_file:
            bunny_client = BunnyCDNStorage()

            # Delete the old video if it exists
            if video_url:
                video_file_path = video_url.split(f"{settings.BUNNY_CDN_HOSTNAME}/")[-1]
                bunny_client.delete_object(video_file_path)

            # Find the course and its category for the storage path
            course = next((c for c in courses if str(c['id']) == course_id), None)
            if course:
                category_name = course['category_name'].replace(" ", "_")
                course_name = course['course_name'].replace(" ", "_")
                storage_path = f"{settings.BUNNY_CDN_STORAGE_ZONE_NAME}/{category_name}/{course_name}/"

                # Upload the new video file
                video_url = bunny_client.upload_file(storage_path, video_file, video_file.name)

        # Update the lesson in the database
        query = """
            UPDATE lessons
            SET title = %s, content = %s, course_id = %s, video_url = %s
            WHERE id = %s
        """
        params = [title, content, course_id, video_url, lesson_id]
        execute_query(query, params)

        return JsonResponse({'success': True, 'redirect_url': reverse('admin_page_app:list_lessons')})

    return render(request, 'admin_page_app/admin_lesson_update.html', {'lesson': lesson, 'courses': courses})



#--------------------------------- End: update views record from the system ---------------------------------#

#--------------------------------- 5) Start: delete views record from the system ---------------------------------#

# 5.1) Delete a category
def delete_category(request, category_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            # Assuming execute_query() is a utility function you've defined to execute raw SQL queries
            execute_query("DELETE FROM categories WHERE id = %s", [category_id])

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# 5.2) Delete a course
def delete_course(request, course_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            # Delete the course using SQL
            query = "DELETE FROM courses WHERE id = %s"
            execute_query(query, [course_id])

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method or headers.'})
    
# 5.3) Delete a payment
def delete_payment(request, payment_id):
    if request.method == 'POST':
        # Delete the payment
        execute_query("DELETE FROM payments WHERE id = %s", [payment_id])
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

# 5.4) Delete a lesson
def delete_lesson(request, lesson_id):
    if request.method == 'POST':
        # Fetch the lesson from the database
        lesson = execute_query("SELECT * FROM lessons WHERE id = %s", [lesson_id], fetchone=True)

        if lesson:
            # Delete video from BunnyCDN if it exists
            if lesson['video_url']:
                # Extract storage path and file name from video URL
                video_file_path = lesson['video_url'].replace(f'https://{settings.BUNNY_CDN_HOSTNAME}/', '')
                
                try:
                    bunny_client = BunnyCDNStorage()
                    bunny_client.delete_object(video_file_path)
                except Exception as error:
                    return JsonResponse({'success': False, 'error': f"Error deleting video: {error}"})

            # Delete the lesson from the database
            execute_query("DELETE FROM lessons WHERE id = %s", [lesson_id])

            return JsonResponse({'success': True, 'message': 'Lesson deleted successfully.'})
        else:
            return JsonResponse({'success': False, 'error': 'Lesson not found.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


#--------------------------------- End: delete views record from the system ---------------------------------#
# 
