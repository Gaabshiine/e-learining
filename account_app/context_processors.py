from .utils import execute_query  # Import the execute_query function
from django.conf import settings  # Import the settings module
import os  # Import the os module

def instructor_context(request):
    """
    Provides context variables for instructor users.
    """
    instructor_user = None
    if 'instructor_id' in request.session:
        query = "SELECT * FROM instructors WHERE id = %s"
        instructor_user = execute_query(query, [request.session['instructor_id']], fetchone=True)

    courses = []
    if instructor_user:
        courses_query = "SELECT * FROM courses WHERE instructor_id = %s"
        courses = execute_query(courses_query, [instructor_user['id']], fetchall=True)

    return {
        'instructor_user': instructor_user,
        'courses': courses,
    }

def student_context(request):
    student_user = None
    profile_picture_url = None

    # Check if student_id is in session
    if 'student_id' in request.session:
        student_id = request.session['student_id']
        query = "SELECT * FROM students WHERE id = %s"
        student_user = execute_query(query, [student_id], fetchone=True)

        if student_user:
            profile_query = "SELECT * FROM profiles WHERE user_id = %s AND user_type = 'student'"
            profile = execute_query(profile_query, [student_user['id']], fetchone=True)
            if profile:
                profile_picture_url = os.path.join(settings.MEDIA_URL, profile['profile_picture']).replace('\\', '/') if profile.get('profile_picture') else None

    return {
        'student_user': student_user,
        'profile_picture_url': profile_picture_url,
    }


