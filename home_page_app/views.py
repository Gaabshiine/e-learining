from django.shortcuts import render, redirect
from django.contrib import messages
from account_app.models import Student
from account_app.utils import execute_query
from django.conf import settings
import os
from django.urls import reverse






# Create your views here.

# -----------------------------------------------------> 1) Start: Home Page <-----------------------------------------------------
# 1.1) Home Page

def home_view(request):
    return render(request, 'home_page_app/index.html')


def about_view(request):
    return render(request, "home_page_app/about.html")


def contact_view(request):
    return render(request, "home_page_app/contact.html")


def membership_view(request):
    return render(request, "home_page_app/membership_plans.html")


def faqs_view(request):
    return render(request, "home_page_app/FAQs.html")

# -----------------------------------------------------> 1) Start: Student Dashboard and Profile <-----------------------------------------------------

# 1.1) Student Dashboard
def student_dashboard(request, student_id):
    """
    View for the student dashboard. Retrieves student profile and passes it to the template.
    """
    return render(request, 'home_page_app/dashboard_student_dashboard.html')
# -----------------------------------------------------> End: Student Dashboard and Profile <-----------------------------------------------------


# -----------------------------------------------------> 2) Start: Intructor Dashboard <-----------------------------------------------------
# def instructor_dashboard(request):
#     """
#     View for the instructor dashboard. Retrieves instructor profile and passes it to the template.
#     """
#     instructor_profile = None

#     # Check if the instructor_id is set in the session
#     if 'instructor_id' in request.session:
#         # Fetch instructor profile from the database
#         query = "SELECT * FROM instructors WHERE id = %s"
#         instructor_profile = execute_query(query, [request.session['instructor_id']], fetchone=True)

#     if not instructor_profile:
#         # If no instructor is found, redirect to the login page
#         return redirect(reverse('account_app:instructor_login'))

#     # Fetch or create the instructor's profile
#     profile_query = "SELECT * FROM profiles WHERE user_id = %s AND user_type = 'instructor'"
#     profile = execute_query(profile_query, [instructor_profile['id']], fetchone=True)

#     # Construct the profile picture URL
#     profile_picture_url = os.path.join(settings.MEDIA_URL, profile['profile_picture']).replace('\\', '/') if profile and profile.get('profile_picture') else None

#     # Add context for the instructor profile
#     context = {
#         'instructor_user': instructor_profile,
#         'profile_picture_url': profile_picture_url,
#     }

#     return render(request, 'instructor_page_app/instructor_dashboard.html', context)

# -----------------------------------------------------> End: Intructor Dashboard <-----------------------------------------------------

def event_list_view(request):
    return render(request, "home_page_app/event_list.html")

def event_detail_view(request, id):
    return render(request, "home_page_app/event_detail.html", {'id': id})


def zoom_meeting_list_view(request):
    return render(request, "home_page_app/zoom_meeting_list.html")

def zoom_meeting_detail_view(request, id):
    return render(request, "home_page_app/zoom_meeting_detail.html", {'id': id})


def course_list_view(request):
    return render(request, "home_page_app/course_list.html")

def course_detail_view(request, id):
    return render(request, "home_page_app/course_detail.html", {'id': id})

def course_category_view(request, id):
    return render(request, "home_page_app/course_category.html", {'id': id})



def instructor_list_view(request):
    return render(request, "home_page_app/instructor_list.html")

def instructor_detail_view(request, id):
    return render(request, "home_page_app/intructor_details.html", {'id': id})




def purchase_view(request):
    return render(request, "home_page_app/purchase.html")


def checkout_view(request):
    return render(request, "home_page_app/checkout.html")









def enrolled_courses(request, id):
    return render(request, "home_page_app/dashboard_enrolled_courses.html", {'id': id})


def wish_list(request, id):
    return render(request, "home_page_app/dashboard_wish_list.html", {'id': id})


def review_view(request, id):
    return render(request, "home_page_app/dashboard_review.html", {'id': id})


def quiz_attempts(request, id):
    return render(request, "home_page_app/dashboard_quiz_attempts.html", {'id': id})

def quiz_attempt_detail(request, id):
    return render(request, "home_page_app/dashboard_quiz_attempt_detail.html", {'id': id})


def purchase_history(request, id):
    return render(request, "home_page_app/dashboard_purchase_history.html", {'id': id})


def certificates_view(request, id):
    return render(request, 'home_page_app/dashboard_certificates.html', {id: id})





