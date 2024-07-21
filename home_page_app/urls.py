# urls.py
from django.urls import path
from . import views


app_name = "home_page_app"

urlpatterns = [
    path("", views.home_view, name="home"),

    path("about/", views.about_view, name="about"),

    path("contact/", views.contact_view, name="contact"),

    path("membership/", views.membership_view, name="membership"),

    path("faqs/", views.faqs_view, name="faqs"),

    # event urls
    path("event_list/", views.event_list_view, name="event_list"),
    path("event_detail/<int:id>/", views.event_detail_view, name="event_detail"),


    path("zoom_meeting_list/", views.zoom_meeting_list_view, name="zoom_meeting_list"),
    path("zoom_meeting_detail/<int:id>/", views.zoom_meeting_detail_view, name="zoom_meeting_detail"),

    # course details
    path("course_list/", views.course_list_view, name="course_list"),
    path("course_detail/<int:id>/", views.course_detail_view, name="course_detail"),
    path("course_category/<int:id>/", views.course_category_view, name="course_category"),

    # intructors
    path("instructor_list/", views.instructor_list_view, name="instructor_list"),
    path("instructor_detail/<int:id>/", views.instructor_detail_view, name="instructor_detail"),
    

]
