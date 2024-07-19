# urls.py
from django.urls import path
from . import views


app_name = "home_page_app"

urlpatterns = [
    path("", views.home_view, name="home"),
]
