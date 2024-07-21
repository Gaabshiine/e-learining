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
]
